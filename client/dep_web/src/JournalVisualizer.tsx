import React, { useState } from 'react';
import {
  ChevronRight,
  ChevronDown,
  Code,
  Variable,
  Repeat,
  ArrowRight,
  Printer,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  LucideIcon
} from 'lucide-react';

// Type definitions for journal events
interface JournalEvent {
  type: string;
  children?: JournalEvent[];
  [key: string]: any;
}

// Event type configuration
const EVENT_TYPES: Record<string, {
  friendlyName: string;
  icon?: LucideIcon | ((event: JournalEvent) => LucideIcon);
  descriptionFormatter?: (event: JournalEvent) => string;
}> = {
  FUNCTION_CALL: {
    friendlyName: "Function Call",
    icon: Code,
    descriptionFormatter: (event) =>
      `${event.name}(${event.params ? event.params.join(', ') : ''})`
  },
  VARIABLE_ASSIGNMENT: {
    friendlyName: "Variable Update",
    icon: Variable,
    descriptionFormatter: (event) =>
      `${event.var_name} ← ${event.after} (was ${event.before})`
  },
  FOR: {
    friendlyName: "Loop Start",
    icon: Repeat,
    descriptionFormatter: (event) =>
      `Iterate: ${event.condition}`
  },
  FOR_ITERATION: {
    friendlyName: "Loop Iteration",
    icon: ArrowRight,
    descriptionFormatter: (event) =>
      `Current value: ${event.iterator}`
  },
  WHILE: {
    friendlyName: "While Loop",
    icon: Repeat,
    descriptionFormatter: (event) =>
      `Condition: ${event.condition || 'Unknown'}`
  },
  WHILE_ITERATION: {
    friendlyName: "While Iteration",
    icon: ArrowRight
  },
  PRINT: {
    friendlyName: "Print",
    icon: Printer,
    descriptionFormatter: (event) =>
      `${event.value}`
  },
  ERROR: {
    friendlyName: "Error",
    icon: AlertTriangle,
    descriptionFormatter: (event) =>
      `${event.info}`
  },
  IF: {
    friendlyName: "If",
    icon: CheckCircle2,
    descriptionFormatter: (event) =>
      `${event.hit ? 'Condition Met' : 'Condition Skipped'}: ${event.condition || ''}`
  },
  ELSE: {
    friendlyName: "Alternative Path",
    icon: XCircle
  },
  SWAP: {
    friendlyName: "Variable Swap",
    icon: Variable,
    descriptionFormatter: (event) =>
      `${event.var_names[0]} ↔ ${event.var_names[1]}`
  },
  DEFAULT: {
    friendlyName: "Event",
    icon: undefined
  }
};

// Color mapping for different event types
const EVENT_COLORS: Record<string, string> = {
  FUNCTION_CALL: '#3B82F6',     // Blue
  VARIABLE_ASSIGNMENT: '#10B981', // Green
  FOR: '#A78BFA',               // Purple
  FOR_ITERATION: '#A78BFA',     // Light Purple
  WHILE: '#F97316',             // Orange
  WHILE_ITERATION: '#e09363',
  PRINT: '#EAB308',             // Yellow
  ERROR: '#EF4444',             // Red
  IF: '#10B981',
  DEFAULT: '#bec0cc'            // Gray
};

// Utility to generate color variations
const generateColorVariants = (baseColor: string) => {
  // If no color is provided, use default gray
  baseColor = baseColor || EVENT_COLORS.DEFAULT;

  // Convert hex to RGB
  const r = parseInt(baseColor.slice(1, 3), 16);
  const g = parseInt(baseColor.slice(3, 5), 16);
  const b = parseInt(baseColor.slice(5, 7), 16);

  // Create border color (slightly lighter)
  const borderColor = `rgb(${Math.min(r + 30, 255)}, ${Math.min(g + 30, 255)}, ${Math.min(b + 30, 255)})`;

  // Create gradient from lighter to darker
  return {
    border: borderColor,
    background: `rgba(${r},${g},${b},0.1)`
  };
};

// Utility to get event-specific color
const getEventColor = (eventType: string) =>
  EVENT_COLORS[eventType] || EVENT_COLORS.DEFAULT;

// Main Event Component
const EventNode: React.FC<{
  event: JournalEvent,
  depth?: number
}> = ({ event, depth = 0 }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const hasChildren = event.children && event.children.length > 0;

  // Get event type configuration
  const eventTypeConfig = EVENT_TYPES[event.type] || EVENT_TYPES.DEFAULT;
  const Icon = eventTypeConfig.icon;

  // Get color for this event type
  const eventColor = getEventColor(event.type);
  const colors = generateColorVariants(eventColor);

  // Determine if event can be expanded
  const isExpandable = hasChildren;

  // Generate description
  const description = eventTypeConfig.descriptionFormatter
    ? eventTypeConfig.descriptionFormatter(event)
    : '';

  return (
    <div
      className={`
        rounded-lg 
        border-1
        shadow-sm 
        mb-2 
        p-2 
        ml-${depth * 4}
      `}
      style={{ color: colors.border, background: colors.background }}
    >
      <div
        className={`flex items-center ${isExpandable ? "cursor-pointer" : "cursor-auto"}`}
        onClick={() => isExpandable && setIsExpanded(!isExpanded)}
      >
        <div className='flex justify-between items-center container px-1'>
          <div className='flex flex-column items-center'>
            {// @ts-ignore
            Icon && <Icon className="mr-2" size={16} />}

            <span className="ml-1 font-semibold">
              {eventTypeConfig.friendlyName}
              {event.var_name ? ` (${event.var_name})` : ''}
            </span>

            {description && (
              <div className="text-sm text-white ml-6">
                {description}
              </div>
            )}
          </div>

          {isExpandable ? (
            isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />
          ) : <div className="w-4"></div>}
        </div>
      </div>

      {/* Nested Children */}
      {isExpanded && hasChildren && (
        <div className="mt-2 space-y-1">
          {event.children!.map((childEvent, index) => (
            <EventNode
              key={index}
              event={childEvent}
              depth={depth + 1}
            />
          ))}
        </div>
      )}
    </div>
  );
};

// Main Journal Visualizer Component
const JournalVisualizer: React.FC<{ journal: { events: JournalEvent[] } }> = ({
  journal
}) => {
  return (
    <div className="p-4 bg-bg-tonal-a10 rounded-xl shadow-md">
      <h2 className="text-xl font-bold mb-4">Program Execution Journal</h2>
      {journal.events.map((event, index) => (
        <EventNode key={index} event={event} />
      ))}
    </div>
  );
};

export default JournalVisualizer;