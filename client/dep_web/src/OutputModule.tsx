import './OutputModule.css'

export function OutputModule(props: { sendCode: () => void, outputText: string}) {

    return (
        <div className="output-module">
            <div className="output-buttons">
                <button onClick={props.sendCode}>RUNN 🐫🐫🐫🐫</button><br />
                <button onClick={props.sendCode}>DEBUGGGG</button><br />
            </div>
            <div className="output-field border" style={{ whiteSpace: 'pre-line' }}>
                {props.outputText}
            </div>
        </div>
    )
}