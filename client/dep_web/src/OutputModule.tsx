import './OutputModule.css';
import JSONPresenter from './JSONPresenter';
import { Play, Bug, Loader } from 'lucide-react';

export function OutputModule(props: {
    runCode: () => void,
    runDebug: () => void,
    outputText: string,
    isLoading: boolean,
    error: string
}) {
    return (
        <div className="output-module">
            <div className="output-buttons">
                <button
                    onClick={props.runCode}
                    className="run-button"
                    disabled={props.isLoading}
                >
                    <><Play size={16} className="mr-1" /> Run 🐫🐫🐫🐫</>
                </button>
                <button
                    onClick={props.runDebug}
                    className="debug-button"
                    disabled={props.isLoading}
                >
                    <Bug size={16} className="mr-1" /> Debug
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
                        {props.error}
                    </div>
                )}
                {!props.isLoading && !props.error && props.outputText && (
                    <JSONPresenter jsonString={props.outputText} />
                )}
            </div>
        </div>
    );
}