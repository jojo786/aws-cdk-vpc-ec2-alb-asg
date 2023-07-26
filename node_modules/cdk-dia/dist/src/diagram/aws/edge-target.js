"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.EdgeTargetStackExport = exports.EdgeTargetSimpleString = exports.EdgeTarget = void 0;
const aws_diagram_generator_1 = require("./aws-diagram-generator");
class EdgeTarget {
}
exports.EdgeTarget = EdgeTarget;
class EdgeTargetSimpleString extends EdgeTarget {
    constructor(value) {
        super();
        this.value = aws_diagram_generator_1.AwsDiagramGenerator.sanitizeComponentId(value);
    }
    isEqual(other) {
        if (!(other instanceof EdgeTargetSimpleString))
            return false;
        return this.value == other.value;
    }
    toString() {
        return `EdgeTargetSimpleString: ${this.value}`;
    }
}
exports.EdgeTargetSimpleString = EdgeTargetSimpleString;
class EdgeTargetStackExport extends EdgeTarget {
    constructor(stackId, exportValue) {
        super();
        this.stackId = stackId;
        this.exportValue = exportValue;
    }
    static fromFnImportValue(value) {
        const matches = value.match(/([^:]*):(.*)/);
        if (!matches)
            throw new Error(`FnImportValue not in expected form: ${value}`);
        return new EdgeTargetStackExport(matches[1], matches[2]);
    }
    isEqual(other) {
        if (!(other instanceof EdgeTargetStackExport))
            return false;
        return this.exportValue == other.exportValue && this.stackId == other.stackId;
    }
    toString() {
        return `EdgeTargetStackExport: ${this.stackId} ${this.exportValue}`;
    }
}
exports.EdgeTargetStackExport = EdgeTargetStackExport;
//# sourceMappingURL=edge-target.js.map