import { useRef, useEffect, Dispatch, SetStateAction } from 'react';
import Markdown from 'react-markdown';
import './dark-mode-markdown.css';

const TutorialModal = ({ isOpen, setIsOpen }: {
  isOpen: boolean;
  setIsOpen: Dispatch<SetStateAction<boolean>>;
}) => {
  const modalRef = useRef(null);

  // Handle clicking outside the modal
  useEffect(() => {
    const handleClickOutside = (event: Event) => {
      // @ts-ignore
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    // Add event listener when modal is open
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    // Cleanup the event listener
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const tutorialContent = `
Welcome! 🐫🐫🐫\n
This is a student project made to help track and execute university-style pseudocode. We built a custom interpreter that is kinda influenced by standard pseudocode syntax
and nomenclature.\n

## Journal\n\n
After running the code, you'll see (what we called) a "Journal", that lists all the actions taken by your code as it runs - variable assignments, for loop iterations, errors, prints and more.
The "Run" mode will only display print and error events, and the "Debug" mode will display all of them.
## Syntax\n\n

### Declaring variables:
We use arrow notation to assign variables:
\`\`\`
x <- [1,2,3,4]
i <- 1.5
i <- i + 1
\`\`\`

### Prints:
\`\`\`
print("Gamal")
\`\`\`

### Loops:
Like Python and most pseudocode found online, we use indentation for blocks:
\`\`\`
while (i < 5)
    i <- i + 1
\`\`\`
For loops are WIP 🦐

### Functions:
Functions are declared with just their name, and their paremeters.
\`\`\`
greet(name)
    print("Hello,", name)
\`\`\`

## Example Code \n\n
Try out the following code and figure out what it does:
\`\`\`
what(n)
    if n = 0
        return True
    else
        return n * what(n - 1)

what(10)
\`\`\`
  `;

  return (
    <>
      {/* Modal Overlay */}
      {isOpen && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          {/* Modal Content */}
          <div 
            ref={modalRef}
            className="markdown-body border-1 border-bg-color-a50 dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-16 relative shadow-xl text-start"
          >
            {/* Close Button */}
            <button 
              onClick={() => setIsOpen(false)}
              className="absolute top-4 right-4 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white"
            >
              ✕
            </button>

            {/* Modal Header */}
            <h1 className="text-2xl font-bold mb-4 border-b pb-2">
              Product Tutorial
            </h1>

            {/* Markdown Content */}
            <div className="prose dark:prose-invert prose-sm sm:prose-base">
              <Markdown 
                components={{
                  img: ({node, ...props}) => (
                    <img 
                      {...props} 
                      className="rounded-lg shadow-md mx-auto my-4 block max-w-full h-auto" 
                      alt={props.alt || "Tutorial image"}
                    />
                  )
                }}
              >
                {tutorialContent}
              </Markdown>

            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default TutorialModal;