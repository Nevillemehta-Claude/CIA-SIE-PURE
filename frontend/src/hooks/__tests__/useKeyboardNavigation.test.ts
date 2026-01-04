import { renderHook } from '@testing-library/react'
import { useKeyboardNavigation, makeClickableAccessible } from '../useKeyboardNavigation'

describe('useKeyboardNavigation', () => {
  it('should call onEnter when Enter key is pressed', () => {
    const onEnter = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onEnter }))

    const event = { key: 'Enter', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onEnter).toHaveBeenCalled()
    expect(event.preventDefault).toHaveBeenCalled()
  })

  it('should call onSpace when Space key is pressed', () => {
    const onSpace = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onSpace }))

    const event = { key: ' ', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onSpace).toHaveBeenCalled()
  })

  it('should call onEscape when Escape key is pressed', () => {
    const onEscape = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onEscape }))

    const event = { key: 'Escape', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onEscape).toHaveBeenCalled()
  })

  it('should call arrow key handlers', () => {
    const onArrowUp = jest.fn()
    const onArrowDown = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onArrowUp, onArrowDown }))

    result.current.handleKeyDown({ key: 'ArrowUp', preventDefault: jest.fn() } as unknown as React.KeyboardEvent)
    result.current.handleKeyDown({ key: 'ArrowDown', preventDefault: jest.fn() } as unknown as React.KeyboardEvent)

    expect(onArrowUp).toHaveBeenCalled()
    expect(onArrowDown).toHaveBeenCalled()
  })

  it('should not call handler for unmapped keys', () => {
    const onEnter = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onEnter }))

    const event = { key: 'Tab', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onEnter).not.toHaveBeenCalled()
  })
})

describe('makeClickableAccessible', () => {
  it('should return correct role and tabIndex', () => {
    const props = makeClickableAccessible(() => {})
    expect(props.role).toBe('button')
    expect(props.tabIndex).toBe(0)
  })

  it('should call onClick on Enter or Space', () => {
    const onClick = jest.fn()
    const props = makeClickableAccessible(onClick)

    props.onKeyDown({ key: 'Enter', preventDefault: jest.fn() } as unknown as React.KeyboardEvent)
    props.onKeyDown({ key: ' ', preventDefault: jest.fn() } as unknown as React.KeyboardEvent)

    expect(onClick).toHaveBeenCalledTimes(2)
  })

  it('should not call onClick on other keys', () => {
    const onClick = jest.fn()
    const props = makeClickableAccessible(onClick)

    props.onKeyDown({ key: 'Tab', preventDefault: jest.fn() } as unknown as React.KeyboardEvent)

    expect(onClick).not.toHaveBeenCalled()
  })
})
