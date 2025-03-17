import CodeMirror from "@uiw/react-codemirror";
import './CodeModule.css';
import { aura } from '@uiw/codemirror-theme-aura';

export function CodeModule(props: { value: string, onChange: (value: string) => void }) {
    return (
        <div className="border">
            <CodeMirror
                value={props.value}
                height="100%"
                width="100%"
                className="code-module"
                onChange={props.onChange}
                theme={aura}
            />
        </div>
    );
} 