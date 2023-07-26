"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DiagramComponent = void 0;
const component_1 = require("./component");
class DiagramComponent extends component_1.Component {
    constructor(id, label, parent) {
        super(id);
        this.depth = () => this._parent.depth() + 1;
        this.label = label;
        this._parent = parent;
    }
    parent() {
        return this._parent;
    }
    toSimpleObject() {
        return {
            id: this.id,
            "_image": this.icon,
            isGroup: this.subComponents().length > 0,
            children: Array.from(this.subComponents()).map(it => { return it.toSimpleObject(); }),
            label: this.label,
            edges: Array.from(this.links.getLinkedComponents()).map(component => { return component.id; })
        };
    }
    assureIdDoesNotExistInConnectedComponents(id) {
        this._parent.assureIdDoesNotExistInConnectedComponents(id);
    }
    setIcon(image) {
        this.icon = image;
    }
    destroyLinks() {
        this.links.getLinkedComponents().forEach(link => {
            this.links.removeLink(link);
        });
        this.links.getReverseLinkedComponents().forEach(linkingComponent => {
            linkingComponent.links.removeLink(this);
        });
    }
    treeRoot() {
        return this.parent().treeRoot();
    }
    treeAncestorInDepth(depth) {
        if (this.depth() == depth)
            return this;
        if (this.depth() < depth || !(this.parent() instanceof DiagramComponent))
            throw Error(`Failed to find an ancestor in depth=${depth} mine=${this.depth()}`);
        return this.parent().treeAncestorInDepth(depth);
    }
}
exports.DiagramComponent = DiagramComponent;
//# sourceMappingURL=diagram-component.js.map