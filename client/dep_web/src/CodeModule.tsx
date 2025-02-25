import CodeMirror from "@uiw/react-codemirror";
import './CodeModule.css';

export function CodeModule(props: {value: string, onChange: (value: string) => void}) {
    return (
        <CodeMirror
            value={props.value}
            height="100%"
            width="100%"
            className="code-module"
            onChange={props.onChange}
        />
    );
}