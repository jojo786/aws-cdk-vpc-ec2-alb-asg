"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ColorPalette = void 0;
const values_js_1 = __importDefault(require("values.js"));
class ColorPalette {
    static byInd(num) {
        const color = new values_js_1.default('#F3F3F3');
        const shade = color.shade(6 * num);
        return shade.hexString();
    }
}
exports.ColorPalette = ColorPalette;
//# sourceMappingURL=styling.js.map