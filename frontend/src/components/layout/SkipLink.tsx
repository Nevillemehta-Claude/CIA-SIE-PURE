/**
 * SkipLink Component
 * 
 * Provides a skip link for keyboard users to bypass navigation and jump
 * directly to main content. This is a WCAG 2.1 AA requirement.
 * 
 * The link is visually hidden until focused, then becomes visible.
 * When activated, it moves focus to the main content area.
 */
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="
        sr-only
        focus:not-sr-only
        focus:absolute
        focus:top-4
        focus:left-4
        focus:z-50
        focus:px-4
        focus:py-2
        focus:bg-blue-600
        focus:text-white
        focus:rounded-lg
        focus:outline-none
        focus:ring-2
        focus:ring-offset-2
        focus:ring-blue-500
        focus:shadow-lg
      "
    >
      Skip to main content
    </a>
  )
}

