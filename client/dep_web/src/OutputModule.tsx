import './OutputModule.css';
import JSONPresenter from './JSONPresenter';
import { Play, Bug } from 'lucide-react';

export function OutputModule(props: { sendCode: () => void, outputText: string }) {
    return (
        <div className="output-module">
            <div className="output-buttons">
                <button 
                    onClick={props.sendCode}
                    className="run-button"
                >
                    <Play size={16} className="mr-1" /> Run 🐫🐫🐫🐫
                </button>
                <button 
                    onClick={props.sendCode}
                    className="debug-button"
                >
                    <Bug size={16} className="mr-1" /> Debug
                </button>
            </div>
            <div className="output-content">
                <JSONPresenter jsonString={props.outputText} />
            </div>
        </div>
    );
}