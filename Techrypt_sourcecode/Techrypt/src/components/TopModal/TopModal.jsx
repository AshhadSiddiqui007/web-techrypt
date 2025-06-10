import React, { useEffect } from 'react'
import { MdOutlineCancel } from 'react-icons/md';

export default function TopModal({ children, isOpen, onClose }) {
    useEffect(() => {
        if (isOpen) {
            document.documentElement.classList.add('overflow-hidden');
            // Optional: Store scroll position to return to later
            const scrollY = window.scrollY;
            document.body.style.position = 'fixed';
            document.body.style.top = `-${scrollY}px`;
            document.body.style.width = '100%';

            return () => {
                document.documentElement.classList.remove('overflow-hidden');
                const scrollY = document.body.style.top;
                document.body.style.position = '';
                document.body.style.top = '';
                document.body.style.width = '';
                window.scrollTo(0, parseInt(scrollY || '0') * -1);
            };
        }
    }, [isOpen]);
    return (
        <div className={`${isOpen ? "translate-y-0" : "-translate-y-full"} transition-all duration-300 bg-black fixed inset-0 flex items-center justify-center z-50 `}>
            <MdOutlineCancel className=" text-white text-3xl cursor-pointer transition-all duration-300  hover:text-primary absolute top-36 right-10 md:right-40" onClick={onClose} />
            <div>
                {children}

            </div>
        </div>
    )
}
