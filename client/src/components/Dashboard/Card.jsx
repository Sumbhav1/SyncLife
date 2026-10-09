
import React from "react";

export const Card = React.forwardRef(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={`rounded-xl p-4 shadow ${className}`} {...props} />
  )
);

Card.displayName = "Card";

