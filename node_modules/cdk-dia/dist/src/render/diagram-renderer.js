"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.RenderingError = exports.RenderingProps = void 0;
class RenderingProps {
}
exports.RenderingProps = RenderingProps;
class RenderingError extends Error {
    constructor(message, debugInfo = [], fixTips = []) {
        super(message);
        Object.setPrototypeOf(this, new.target.prototype);
        this.name = RenderingError.name;
        this.debugInfo = debugInfo;
        this.fixTips = fixTips;
    }
}
exports.RenderingError = RenderingError;
//# sourceMappingURL=diagram-renderer.js.map