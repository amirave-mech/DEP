import React from 'react';
import './JournalVisualizer.css';

interface Event {
  type: string;
  name?: string;
  timestamp?: number;
  children?: Event[];
  
  // New Frontend Event Properties
  hit?: boolean; // For IF events
  condition?: string; // For IF, FOR, WHILE events
  iteration_count?: number; // For FOR, WHILE events
  iterator?: any; // For FOR_ITERATION
  
  var_name?: string; // For VARIABLE_ASSIGNMENT
  before?: any; // For VARIABLE_ASSIGNMENT
  after?: any; // For VARIABLE_ASSIGNMENT
  
  value?: any; // For PRINT events
  
  params?: any[]; // For FUNCTION_CALL
  return_value?: any; // For FUNCTION_CALL
  
  info?: string; // For ERROR events
  
  var_names?: [string, string]; // For SWAP events
  values?: [any, any]; // For SWAP events
  
  index?: number | string; // For ARRAY_MODIFICATION
  arr_before?: any[]; // For ARRAY_MODIFICATION
  arr_after?: any[]; // For ARRAY_MODIFICATION
}

interface Journal {
  events: Event[];
  metadata: {
    totalEvents: number;
    maxDepthReached: boolean;
    maxLengthReached: boolean;
    error?: boolean;
  };
}

interface JournalVisualizerProps {
  journal: Journal;
}

const JournalVisualizer: React.FC<JournalVisualizerProps> = ({ journal }) => {
  if (!journal) {
    return null;
  }
  return (
    <div className="journal-visualizer">
      {journal.events.map((event, index) => (
        <EventRenderer key={index} event={event} depth={0} />
      ))}
    </div>
  );
};

interface EventRendererProps {
  event: Event;
  depth: number;
}

const EventRenderer: React.FC<EventRendererProps> = ({ event, depth }) => {
  const renderEventContent = () => {
    switch (event.type) {
      case 'IF':
        return (
          <div className={`condition-block ${event.hit === false ? 'condition-false' : ''} ${depth > 0 ? 'nested-step' : ''}`}>
            <div>
              If: {event.hit ? 'True' : 'False'}
              {/* {event.hit === false ? <span style={{color: 'red'}}>✗</span> : <span style={{color: 'green'}}>✓</span>}  */}
            </div>
            {event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'ELSE':
        return (
          <div className={`else-block ${depth > 0 ? 'nested-step' : ''}`}>
            <div>Else block</div>
            {event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'FOR':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>
              for {event.condition}
              {event.iteration_count !== undefined && ` (${event.iteration_count} iterations)`}
            </div>
            {event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'FOR_ITERATION':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>Iteration: {JSON.stringify(event.iterator)}</div>
            {event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'WHILE':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>
              while {event.condition}
              {event.iteration_count !== undefined && ` (${event.iteration_count} iterations)`}
            </div>
            {event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'WHILE_ITERATION':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>While Iteration</div>
            {event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'VARIABLE_ASSIGNMENT':
        return (
          <div className={`variable-assignment ${depth > 0 ? 'nested-step' : ''}`}>
            {event.var_name} = {JSON.stringify(event.after)}
            {event.before !== null && event.before !== undefined && (
              <span className="text-gray-500 text-sm"> (was: {JSON.stringify(event.before)})</span>
            )}
          </div>
        );

      case 'PRINT':
        return (
          <div className={`print-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>Print: <span>{JSON.stringify(event.value)}</span></div>
          </div>
        );

      case 'FUNCTION_CALL':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>
              {event.name}({event.params ? event.params.map(p => JSON.stringify(p)).join(', ') : ''})
              {event.return_value !== undefined && 
                ` → ${JSON.stringify(event.return_value)}`}
            </div>
            {event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'ERROR':
        return (
          <div className={`error-block ${depth > 0 ? 'nested-step' : ''}`}>
            <div style={{color: 'red'}}>Error: {event.info}</div>
          </div>
        );

      case 'SWAP':
        return (
          <div className={`swap-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>
              Swap: {event.var_names?.[0]} ↔ {event.var_names?.[1]} 
              ({JSON.stringify(event.values?.[0])} ↔ {JSON.stringify(event.values?.[1])})
            </div>
          </div>
        );

      case 'ARRAY_MODIFICATION':
        return (
          <div className={`array-modification ${depth > 0 ? 'nested-step' : ''}`}>
            <div>
              Array[{event.index}] modified 
              from {JSON.stringify(event.arr_before)} 
              to {JSON.stringify(event.arr_after)}
            </div>
          </div>
        );

      default:
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <pre>{JSON.stringify(event, null, 2)}</pre>
          </div>
        );
    }
  };

  return renderEventContent();
};

export default JournalVisualizer;