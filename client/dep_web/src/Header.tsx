import {
    Info
  } from 'lucide-react';

function Header({onOpenTutorial}: any) {
    return (
        <div className='header'>
            <img src='public/logo.png' />
            <div>
                <button className='flex flex-column gap-1 items-center' onClick={onOpenTutorial}>
                    <p>Tutorial</p>
                    <Info size={'1rem'}></Info>
                </button>
            </div>
            {/* <h1 className='title'>Pcode</h1> */}
        </div>
    )
}

export default Header;