import { useCallback, KeyboardEvent } from 'react'

interface UseKeyboardNavigationOptions {
  onEnter?: () => void
  onSpace?: () => void
  onEscape?: () => void
  onArrowUp?: () => void
  onArrowDown?: () => void
  onArrowLeft?: () => void
  onArrowRight?: () => void
}

/**
 * Hook for consistent keyboard navigation handling across the application.
 * Provides standardized keyboard event handling for accessibility.
 */
export const useKeyboardNavigation = (options: UseKeyboardNavigationOptions) => {
  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      switch (event.key) {
        case 'Enter':
          if (options.onEnter) {
            event.preventDefault()
            options.onEnter()
          }
          break
        case ' ':
          if (options.onSpace) {
            event.preventDefault()
            options.onSpace()
          }
          break
        case 'Escape':
          if (options.onEscape) {
            event.preventDefault()
            options.onEscape()
          }
          break
        case 'ArrowUp':
          if (options.onArrowUp) {
            event.preventDefault()
            options.onArrowUp()
          }
          break
        case 'ArrowDown':
          if (options.onArrowDown) {
            event.preventDefault()
            options.onArrowDown()
          }
          break
        case 'ArrowLeft':
          if (options.onArrowLeft) {
            event.preventDefault()
            options.onArrowLeft()
          }
          break
        case 'ArrowRight':
          if (options.onArrowRight) {
            event.preventDefault()
            options.onArrowRight()
          }
          break
      }
    },
    [options]
  )

  return { handleKeyDown }
}

/**
 * Utility function to make div elements behave like accessible buttons.
 * Use this when you need a div to act as a clickable element.
 * 
 * @example
 * <div {...makeClickableAccessible(() => handleClick())}>
 *   Click me
 * </div>
 */
export const makeClickableAccessible = (onClick: () => void) => ({
  role: 'button' as const,
  tabIndex: 0,
  onClick,
  onKeyDown: (e: KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      onClick()
    }
  },
})

