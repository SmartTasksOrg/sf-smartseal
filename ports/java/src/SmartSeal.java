import java.nio.file.*;
import java.security.MessageDigest;
import java.util.*;

/*
 * SmartSeal - native Java port. Reproduces sf_smartseal.core.seal/verify
 * (SHA-256 digest, 32-hex signature = sha256(digest+signer), tamper/valid). JDK-only.
 *   javac SmartSeal.java && java SmartSeal [vectors.json]
 */
public class SmartSeal {

    static String sha(String s) throws Exception {
        byte[] d = MessageDigest.getInstance("SHA-256").digest(s.getBytes("UTF-8"));
        StringBuilder b = new StringBuilder();
        for (byte x : d) b.append(String.format("%02x", x));
        return b.toString();
    }

    static Map<String, Object> seal(String content, String signer) throws Exception {
        String digest = sha(content);
        String sig = sha(digest + signer).substring(0, 32);
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("sha256", digest); m.put("signature", sig); m.put("chain", List.of(signer));
        return m;
    }

    static Map<String, Object> verify(String content, String recSha, String recSig, int chainLen, String signer) throws Exception {
        String now = sha(content);
        boolean tampered = !now.equals(recSha);
        String expected = sha(recSha + signer).substring(0, 32);
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("valid", !tampered && expected.equals(recSig));
        m.put("tampered", tampered); m.put("chain_len", chainLen);
        return m;
    }

    static String esc(String s) {
        StringBuilder b = new StringBuilder();
        for (char c : s.toCharArray()) switch (c) {
            case '"' -> b.append("\\\""); case '\\' -> b.append("\\\\");
            case '\n' -> b.append("\\n"); case '\r' -> b.append("\\r"); case '\t' -> b.append("\\t");
            default -> b.append(c);
        }
        return b.toString();
    }

    @SuppressWarnings("unchecked")
    static String toJson(Object o) {
        if (o == null) return "null";
        if (o instanceof String s) return "\"" + esc(s) + "\"";
        if (o instanceof Boolean || o instanceof Integer || o instanceof Long) return o.toString();
        if (o instanceof List<?> l) {
            StringBuilder b = new StringBuilder("[");
            for (int i = 0; i < l.size(); i++) { if (i > 0) b.append(","); b.append(toJson(l.get(i))); }
            return b.append("]").toString();
        }
        Map<String, Object> m = (Map<String, Object>) o;
        StringBuilder b = new StringBuilder("{"); boolean first = true;
        for (var e : m.entrySet()) { if (!first) b.append(","); first = false;
            b.append("\"").append(esc(e.getKey())).append("\":").append(toJson(e.getValue())); }
        return b.append("}").toString();
    }

    public static void main(String[] args) throws Exception {
        String vpath = args.length >= 1 ? args[0]
            : Paths.get(System.getProperty("user.dir"), "..", "conformance", "vectors.json").toString();
        Json j = new Json(Files.readString(Paths.get(vpath)));
        Map<String, Object> root = j.parseObject();
        @SuppressWarnings("unchecked")
        List<Object> cases = (List<Object>) root.get("cases");
        List<Object> results = new ArrayList<>();
        for (Object oc : cases) {
            @SuppressWarnings("unchecked")
            Map<String, Object> c = (Map<String, Object>) oc;
            String name = (String) c.get("name");
            String op = (String) c.getOrDefault("op", "seal");
            String signer = (String) c.getOrDefault("signer", "SmartSeal-demo");
            Map<String, Object> out = new LinkedHashMap<>();
            out.put("name", name);
            if (op.equals("seal")) {
                out.putAll(seal((String) c.getOrDefault("content", ""), signer));
            } else {
                Map<String, Object> r = seal((String) c.getOrDefault("seal_content", ""), signer);
                String vsigner = (String) c.getOrDefault("verify_signer", signer);
                out.putAll(verify((String) c.getOrDefault("content", ""),
                    (String) r.get("sha256"), (String) r.get("signature"), 1, vsigner));
            }
            results.add(out);
        }
        Map<String, Object> top = new LinkedHashMap<>();
        top.put("results", results);
        System.out.println(toJson(top));
    }

    static class Json {
        final String s; int i;
        Json(String s) { this.s = s; }
        void ws() { while (i < s.length() && Character.isWhitespace(s.charAt(i))) i++; }
        Map<String, Object> parseObject() { ws(); return (Map<String, Object>) value(); }
        Object value() { ws(); char c = s.charAt(i);
            return switch (c) { case '{' -> obj(); case '[' -> arr(); case '"' -> str();
                case 't', 'f' -> bool(); case 'n' -> nul(); default -> num(); }; }
        Map<String, Object> obj() { Map<String, Object> m = new LinkedHashMap<>(); i++; ws();
            if (s.charAt(i) == '}') { i++; return m; }
            while (true) { ws(); String k = str(); ws(); i++; m.put(k, value()); ws();
                if (s.charAt(i) == ',') { i++; continue; } i++; break; } return m; }
        List<Object> arr() { List<Object> a = new ArrayList<>(); i++; ws();
            if (s.charAt(i) == ']') { i++; return a; }
            while (true) { a.add(value()); ws(); if (s.charAt(i) == ',') { i++; continue; } i++; break; } return a; }
        String str() { StringBuilder b = new StringBuilder(); i++;
            while (true) { char c = s.charAt(i++); if (c == '"') break;
                if (c == '\\') { char e = s.charAt(i++); switch (e) {
                    case '"' -> b.append('"'); case '\\' -> b.append('\\'); case '/' -> b.append('/');
                    case 'n' -> b.append('\n'); case 'r' -> b.append('\r'); case 't' -> b.append('\t');
                    case 'b' -> b.append('\b'); case 'f' -> b.append('\f');
                    case 'u' -> { b.append((char) Integer.parseInt(s.substring(i, i + 4), 16)); i += 4; }
                    default -> b.append(e); } } else b.append(c); }
            return b.toString(); }
        Object bool() { if (s.startsWith("true", i)) { i += 4; return Boolean.TRUE; } i += 5; return Boolean.FALSE; }
        Object nul() { i += 4; return null; }
        Object num() { int st = i; while (i < s.length() && "+-.eE0123456789".indexOf(s.charAt(i)) >= 0) i++;
            return Double.parseDouble(s.substring(st, i)); }
    }
}
