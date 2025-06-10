import React from 'react'

export default function ParallaxWrapper({ children, className }) {
    return (
        <div className='relative'>
       { children?.map((child,i) => (
            <div key={i} className={`sticky top-0 pt-3 md:pt-9 ${className}`}>
                {child}
            </div>
        ))}
        </div>
    )
}
