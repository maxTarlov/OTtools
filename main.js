function edgePhenomenon(side, candidate, category, target){
    function isCorrectCategory(node){
        //TODO: Add support for Ito & Mester style min/max etc
        return node.cat == category;
    }
    function matchesTarget(terminal){
        let regex;
        if (!target) return true;
        switch(target.constructor){
            case RegExp:
                regex = target;
                break;
            case String:
                regex = new RegExp(target);
                break;
            default:
                throw new Error("target must be String or RegExp");
        }
        return regex.test(terminal.id);
    }
    function edgeFactory(edge){
        return function(tree){
            let leaves = getLeaves(tree);
            let result;
            switch(edge){
                case 'left':
                    result = leaves[0];
                    break;
                case 'right':
                    result = leaves[leaves.length - 1];
                    break;
                default:
                    throw new Error('Side not recognized, choose "left" or "right"');
            }
            return result;
        }
    }
    const edgeNodeOf = edgeFactory(side);
    let result = [];
    walkTree(candidate, function(node) {
        if (isCorrectCategory(node) && matchesTarget(edgeNodeOf(node))){
            result.push(edgeNodeOf(node));
        }
    });
    return result;
}