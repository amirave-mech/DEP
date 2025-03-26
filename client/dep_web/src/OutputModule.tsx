import './OutputModule.css';
// import JSONPresenter from './JSONPresenter';
import JournalVisualizer from './JournalVisualizer';
import { Play, Bug, Loader, AlertTriangle } from 'lucide-react';

export function OutputModule(props: {
    runCode: () => void,
    runDebug: () => void,
    outputText: string,
    isLoading: boolean,
    error: string,
    serverMessage?: string
}) {
    return (
        <div className="border output-module">
            <div className="output-buttons">
                <button
                    onClick={props.runCode}
                    className="run-button"
                    disabled={props.isLoading}
                >
                    <><Play size={16} className="mr-1" /> Run 🐫🐫🐫🐫 (F5)</>
                </button>
                <button
                    onClick={props.runDebug}
                    className="debug-button"
                    disabled={props.isLoading}
                >
                    <Bug size={16} className="mr-1" /> Debug (Shift+F5)
                </button>
            </div>
            <div className="output-content">
                {props.isLoading && (
                    <div className="loading-indicator">
                        <Loader className="animate-spin" size={24} /> Loading...
                    </div>
                )}
                {props.error && (
                    <div className="error-message">
                        <div className="flex items-center text-red-600 bg-red-50 p-3 rounded-md mx-auto w-fit">
                            <AlertTriangle className="alert-style" size={24} />
                            <span className="error-type">{props.error}</span>
                        </div>
                        {props.serverMessage && (
                            <div className="server-error-message">
                                <strong>Server Message:</strong> {props.serverMessage}
                            </div>
                        )}
                    </div>
                )}
                {!props.isLoading && !props.error && props.outputText && (
                    // <JSONPresenter jsonString={props.outputText} />
                    <JournalVisualizer journal={JSON.parse(props.outputText)}/>
                )}
            </div>
        </div>
    );
}