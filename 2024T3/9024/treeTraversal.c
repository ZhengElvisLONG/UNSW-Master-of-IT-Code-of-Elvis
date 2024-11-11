void InOrderTraversal2(BiTreeNodePtr root, NodeVisitor visit) {
    // Check if the root is not null (base case)
    if (root) {
        // Create a stack to simulate the recursion manually
        struct Stack *pStack = CreateStack();
        // Set the initial state of the root node to "up" (indicating it has not been visited yet)
        root->state = NS_FROM_UP;

        // Push the root node onto the stack to start traversal
        StackPush(pStack, root);
        
        // Loop until all nodes are processed and the stack is empty
        while (!StackIsEmpty(pStack)) {
            // Peek at the top node in the stack without removing it
            BiTreeNodePtr curNode = StackPeek(pStack);
            
            // Check the current state of curNode to determine which part of it to process
            switch (curNode->state) {
                
            case NS_FROM_UP:
                // Q1: Set state to NS_FROM_LEFT to indicate the next step will be visiting the left subtree
                curNode->state = NS_FROM_LEFT;
                
                // If curNode has a left child, prepare it to be processed next
                if (curNode->leftChild) {
                    // Set the state of the left child to NS_FROM_UP (unvisited)
                    curNode->leftChild->state = NS_FROM_UP;
                    // Push the left child onto the stack for processing
                    StackPush(pStack, curNode->leftChild);
                }
                break;

            case NS_FROM_LEFT:
                // Q3: Visit the curNode as left subtree has been fully processed
                visit(curNode);
                
                // Q4: Update state to NS_FROM_RIGHT, indicating right subtree will be processed next
                curNode->state = NS_FROM_RIGHT;
                
                // If curNode has a right child, prepare it to be processed
                if (curNode->rightChild) {
                    // Set the state of the right child to NS_FROM_UP (unvisited)
                    curNode->rightChild->state = NS_FROM_UP;
                    // Push the right child onto the stack for processing
                    StackPush(pStack, curNode->rightChild);
                }
                break;

            case NS_FROM_RIGHT:
                // Q5: Pop curNode from the stack as both left and right subtrees have been processed
                StackPop(pStack);
                break;

            default:
                // Handle unexpected state (though we expect only NS_FROM_UP, NS_FROM_LEFT, NS_FROM_RIGHT)
                break;
            }
        }
        
        // Clean up: release the memory allocated for the stack
        ReleaseStack(pStack);
    }
}
