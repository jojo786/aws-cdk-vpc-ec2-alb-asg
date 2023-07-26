"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ComponentLinks = void 0;
class ComponentLinks {
    constructor(component) {
        this.links = new Set();
        this.getLinkedComponents = () => Array.from(this.links);
        this.reverseLinks = new Set();
        this.getReverseLinkedComponents = () => Array.from(this.reverseLinks);
        this.component = component;
    }
    addLink(target) {
        this.links.add(target);
        target.links.addReverseLink(this.component);
    }
    removeLink(target) {
        this.links.delete(target);
        target.links.removeReverseLink(this.component);
    }
    updateLinkTarget(prev, next) {
        this.removeLink(prev);
        this.addLink(next);
    }
    addReverseLink(targetComponent) {
        this.reverseLinks.add(targetComponent);
    }
    removeReverseLink(targetComponent) {
        if (!this.reverseLinks.has(targetComponent))
            throw new Error("Actually reverseLink " + targetComponent.id + " isn't in list of " + this.component.id);
        this.reverseLinks.delete(targetComponent);
    }
}
exports.ComponentLinks = ComponentLinks;
//# sourceMappingURL=component-links.js.map