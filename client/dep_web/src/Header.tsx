import {
    Info
  } from 'lucide-react';
import SampleCodes from './SamleCodes';

function Header({onOpenTutorial, onSampleSelect}: {onOpenTutorial: any, onSampleSelect: (code: string) => void}) {
    return (
        <div className='header'>
            <img src='/logo.png' />
            <div className="flex items-center gap-4">
                <button className='flex flex-column gap-1 items-center' onClick={onOpenTutorial}>
                    <p>Tutorial</p>
                    <Info size={'1rem'}></Info>
                </button>
                <SampleCodes onSampleSelect={onSampleSelect} />
            </div>
            {/* <h1 className='title'>Pcode</h1> */}
        </div>
    )
}

export default Header;