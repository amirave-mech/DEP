import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const TutorialModal = ({ isOpen, setIsOpen }) => {
  const modalRef = useRef(null);

  // Handle clicking outside the modal
  useEffect(() => {
    const handleClickOutside = (event) => {
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
# Product Tutorial

## Getting Started

Welcome to our product! This tutorial will guide you through the basic features and how to use them effectively.

### 1. Dashboard Overview
![Dashboard Placeholder](/api/placeholder/600/400)

The main dashboard provides a comprehensive view of your key metrics and activities. Key sections include:
- **Analytics**: Real-time performance tracking
- **Insights**: Detailed data visualizations
- **Quick Actions**: Rapid access to most-used features

### 2. Creating a New Project
![New Project Placeholder](/api/placeholder/600/400)

To create a new project:
1. Click the "New Project" button in the top right corner
2. Fill in the project details
3. Select your project template
4. Click "Create"

### 3. Collaboration Tools
![Collaboration Placeholder](/api/placeholder/600/400)

Our collaboration features make teamwork seamless:
- **Real-time Editing**: Multiple team members can work simultaneously
- **Commenting**: Add inline comments and feedback
- **Version History**: Track changes and revert if needed

### 4. Advanced Settings
![Settings Placeholder](/api/placeholder/600/400)

Customize your experience:
- **User Permissions**: Granular access control
- **Integrations**: Connect with your favorite tools
- **Notifications**: Set up custom alerts

## Tips and Tricks

- Use keyboard shortcuts to navigate faster
- Explore the contextual help icons throughout the interface
- Regularly check our knowledge base for updates

**Pro Tip**: Press \`Ctrl + /\` to open the quick command palette!
  `;

  return (
    <>
      {/* Modal Overlay */}
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          {/* Modal Content */}
          <div 
            ref={modalRef}
            className="bg-white dark:bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto p-6 relative shadow-xl"
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