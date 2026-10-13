// Flowise custom node for SmartSeal (IAIso governance).
// Copy this folder into Flowise's components/nodes/ (or load as a custom tool).
// It shells out to the shipped adapter.py, so smartseal must be importable
// (install SmartSeal from a clone: python -m pip install . ; it is not on PyPI yet)
// or PYTHONPATH set to the repo src/.
const path = require('path');
const { spawnSync } = require('child_process');

class SmartSeal_Node {
  constructor() {
    this.label = 'SmartSeal';
    this.name = 'smartseal_seal';
    this.version = 1.0;
    this.type = 'SmartSeal';
    this.category = 'SmartTasks / IAIso Governance';
    this.description = "Produce a content-addressed SHA-256 receipt (manifest + signature) for a file.";
    this.baseClasses = [this.type, 'Tool'];
    this.inputs = [
      { label: 'Input (file)', name: 'input', type: 'string' },
      { label: 'Python', name: 'python', type: 'string', default: 'python3', optional: true },
    ];
  }

  async init(nodeData) {
    const input = (nodeData.inputs && nodeData.inputs.input) || '';
    const py = (nodeData.inputs && nodeData.inputs.python) || 'python3';
    const adapter = path.join(__dirname, '..', 'adapter.py');
    const res = spawnSync(py, [adapter, '--file', input], { encoding: 'utf8' });
    if (res.status !== 0) throw new Error(res.stderr || 'SmartSeal adapter failed');
    return JSON.parse(res.stdout);
  }
}

module.exports = { nodeClass: SmartSeal_Node };
