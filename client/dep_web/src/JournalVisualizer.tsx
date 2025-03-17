import React from 'react';
import './JournalVisualizer.css';

interface Event {
  type: string;
  name?: string;
  timestamp?: number;
  children?: Event[];
  varName?: string;
  before?: any;
  after?: any;
  value?: any;
  condition?: string;
  result?: boolean;
  returnedValue?: any;
  iterator?: number;
  iterations?: number;
  params?: any[];
  scopeId?: string;
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
    return ('');
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
  // Always expanded, no toggles
  const isExpanded = true;

  const renderEventContent = () => {
    switch (event.type) {
      case 'EXECUTING':
        return (
          <div className={`executing-block ${depth > 0 ? 'nested-step' : ''}`}>
            <div className="font-medium">Executing "{event.name}"...</div>
            {isExpanded && event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'VARIABLE_ASSIGNMENT':
        return (
          <div className={`variable-assignment ${depth > 0 ? 'nested-step' : ''}`}>
            {event.varName} = {JSON.stringify(event.after)}
            {event.before !== null && event.before !== undefined && (
              <span className="text-gray-500 text-sm"> (was: {JSON.stringify(event.before)})</span>
            )}
          </div>
        );

      case 'CONDITION':
        return (
          <div className={`condition-block ${event.result === false ? 'condition-false' : ''} ${depth > 0 ? 'nested-step' : ''}`}>
            <div>
              {event.result === false ? <span style={{color: 'red'}}>✗</span> : <span style={{color: 'green'}}>✓</span>} {event.condition} - {event.result ? 'True' : 'False'}
            </div>
            {isExpanded && event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'WHILE_START':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>while {event.condition}:</div>
            {isExpanded && event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'FOR_START':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>for {event.condition}:</div>
            {isExpanded && event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'FOR_ITERATION_START':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>Iteration {event.iterator}</div>
          </div>
        );

      case 'FOR_ITERATION_END':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>End of iteration</div>
          </div>
        );

      case 'FOR_END':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>Loop completed with {event.iterations} iterations</div>
          </div>
        );

      case 'STEP':
      case 'FUNCTION_CALL':
        return (
          <div className={`code-step ${depth > 0 ? 'nested-step' : ''}`}>
            <div>
              {event.name || "Step"} 
              {event.params && event.params.length > 0 && 
                <span>({event.params.map(p => JSON.stringify(p)).join(', ')})</span>
              }
            </div>
            {isExpanded && event.children && event.children.map((child, idx) => (
              <EventRenderer key={idx} event={child} depth={depth + 1} />
            ))}
          </div>
        );

      case 'RETURN':
        return (
          <div className={`return-value ${depth > 0 ? 'nested-step' : ''}`}>
            {/* Removed the emoji and "Return:" text */}
            {JSON.stringify(event.value || event.returnedValue)}
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