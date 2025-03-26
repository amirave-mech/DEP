import { useRef, useEffect, Dispatch, SetStateAction } from 'react';
import ReactMarkdown from 'react-markdown';

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
Welcome! 
if you reading this, you probably don’t have any idea what is the syntax of the Pcoder:
Syntax

declaring variables:
\`\`\`x <- [1,2,3,4]
i <- 1.5\`\`\`

Print:
\`\`\`print("Gamal")\`\`\`

Loops:
\`\`\`while (i < 5)
    i <- i + 1\`\`\`
currently we don’t have for loops
  `;

  return (
    <>
      {/* Modal Overlay */}
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          {/* Modal Content */}
          <div 
            ref={modalRef}
            className="bg-bg-tonal-a10 dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6 relative shadow-xl text-start"
          >
            {/* Close Button */}
            <button 
              onClick={() => setIsOpen(false)}
              className="absolute top-4 right-4 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white"
            >
              ✕
            </button>

            {/* Modal Header */}
            <h2 className="text-2xl font-bold mb-4 border-b pb-2">
              Product Tutorial
            </h2>

            {/* Markdown Content */}
            <div className="prose dark:prose-invert prose-sm sm:prose-base">
              <ReactMarkdown 
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
              </ReactMarkdown>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default TutorialModal;