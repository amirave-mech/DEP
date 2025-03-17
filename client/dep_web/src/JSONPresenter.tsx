import React from 'react';
import JournalVisualizer from './JournalVisualizer';

interface JSONPresenterProps {
  jsonString: string;
}

const JSONPresenter: React.FC<JSONPresenterProps> = ({ jsonString }) => {
  // Function to parse the JSON string safely
  const parseJournal = () => {
    if (!jsonString) {
      return null;
    }
    try {
      // Clean up the string if needed
      let cleanJson = jsonString;
      
      // Handle cases where the string might contain text before JSON
      if (jsonString.includes('{') && !jsonString.trim().startsWith('{') && !jsonString.trim().startsWith('[')) {
        cleanJson = jsonString.substring(jsonString.indexOf('{'));
      }
      
      // Try to parse the JSON
      const parsedData = JSON.parse(cleanJson);
      
      // Check if this is already in our expected format
      if (parsedData.events) {
        return parsedData;
      }
      
      // If it's an algorithm execution trace, convert it to our format
      if (parsedData.algorithm || parsedData.name || parsedData.type === "EXECUTING") {
        const algorithmName = parsedData.algorithm || parsedData.name || "Algorithm";
        
        return {
          events: [{
            type: "EXECUTING",
            name: algorithmName,
            timestamp: Date.now(),
            children: formatOperations(parsedData.operations || parsedData.steps || parsedData.children || [])
          }],
          metadata: {
            totalEvents: countEvents(parsedData),
            maxDepthReached: false,
            maxLengthReached: false
          }
        };
      }
      
      // If it's an array, assume it's a list of operations
      if (Array.isArray(parsedData)) {
        return {
          events: [{
            type: "EXECUTING",
            name: "Algorithm",
            timestamp: Date.now(),
            children: formatOperations(parsedData)
          }],
          metadata: {
            totalEvents: countEvents({ children: parsedData }),
            maxDepthReached: false,
            maxLengthReached: false
          }
        };
      }
      
      // Default case: wrap whatever we got in our structure
      return {
        events: [{
          type: "EXECUTING",
          name: "Execution Trace",
          timestamp: Date.now(),
          children: [parsedData]
        }],
        metadata: {
          totalEvents: 1,
          maxDepthReached: false,
          maxLengthReached: false
        }
      };
    } catch (error) {
      // Return a fallback structure
      return {
        events: [{
          type: "EXECUTING",
          name: "Error parsing execution trace",
          timestamp: Date.now(),
          children: [{
            type: "ERROR",
            message: `Could not parse JSON: ${error}`,
            raw: jsonString,
            timestamp: Date.now()
          }]
        }],
        metadata: {
          totalEvents: 1,
          error: true,
          maxDepthReached: false,
          maxLengthReached: false
        }
      };
    }
  };
  
  // Format operations/steps to match our event structure
  const formatOperations = (operations: any[]) => {
    return operations.map(op => {
      // Basic mapping
      const formattedOp: any = {
        type: op.type || "STEP",
        timestamp: op.timestamp || Date.now()
      };
      
      // Handle specific operation types
      if (op.variable || op.varName) {
        formattedOp.type = "VARIABLE_ASSIGNMENT";
        formattedOp.varName = op.variable || op.varName;
        formattedOp.before = op.before !== undefined ? op.before : null;
        formattedOp.after = op.after !== undefined ? op.after : op.value;
        formattedOp.value = op.displayValue || op.value;
      } else if (op.condition) {
        formattedOp.type = op.type || "CONDITION";
        formattedOp.condition = op.condition;
        formattedOp.result = op.result || op.hit;
      } else if (op.loop) {
        formattedOp.type = "WHILE_START";
        formattedOp.condition = op.loop;
      } else if (op.return !== undefined || op.value !== undefined) {
        formattedOp.type = "RETURN";
        formattedOp.value = op.return !== undefined ? op.return : op.value;
        formattedOp.returnedValue = op.returnedValue || op.actualValue || op.value;
      }
      
      // Handle children recursively
      if (op.children && Array.isArray(op.children)) {
        formattedOp.children = formatOperations(op.children);
      } else if (op.steps && Array.isArray(op.steps)) {
        formattedOp.children = formatOperations(op.steps);
      } else if (op.operations && Array.isArray(op.operations)) {
        formattedOp.children = formatOperations(op.operations);
      }
      
      return formattedOp;
    });
  };
  
  // Count total events recursively
  const countEvents = (data: any): number => {
    let count = 0;
    
    if (Array.isArray(data)) {
      count += data.length;
      data.forEach(item => {
        if (item.children) count += countEvents(item.children);
        if (item.steps) count += countEvents(item.steps);
        if (item.operations) count += countEvents(item.operations);
      });
    } else if (data.children) {
      count += countEvents(data.children);
    } else if (data.steps) {
      count += countEvents(data.steps);
    } else if (data.operations) {
      count += countEvents(data.operations);
    }
    
    return count;
  };

  // Parse the journal data
  const journalData = parseJournal();

  return (
    <div className="json-presenter h-full overflow-auto bg-gray-50">
      <JournalVisualizer journal={journalData} />
    </div>
  );
};

export default JSONPresenter;