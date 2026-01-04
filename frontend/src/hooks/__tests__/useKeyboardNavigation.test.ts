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
    expect(event.preventDefault).toHaveBeenCalled()
  })

  it('should call onEscape when Escape key is pressed', () => {
    const onEscape = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onEscape }))

    const event = { key: 'Escape', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onEscape).toHaveBeenCalled()
    expect(event.preventDefault).toHaveBeenCalled()
  })

  it('should call onArrowUp when ArrowUp key is pressed', () => {
    const onArrowUp = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onArrowUp }))

    const event = { key: 'ArrowUp', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onArrowUp).toHaveBeenCalled()
  })

  it('should call onArrowDown when ArrowDown key is pressed', () => {
    const onArrowDown = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onArrowDown }))

    const event = { key: 'ArrowDown', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onArrowDown).toHaveBeenCalled()
  })

  it('should call onArrowLeft when ArrowLeft key is pressed', () => {
    const onArrowLeft = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onArrowLeft }))

    const event = { key: 'ArrowLeft', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onArrowLeft).toHaveBeenCalled()
  })

  it('should call onArrowRight when ArrowRight key is pressed', () => {
    const onArrowRight = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onArrowRight }))

    const event = { key: 'ArrowRight', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onArrowRight).toHaveBeenCalled()
  })

  it('should not call any handler if key is not mapped', () => {
    const onEnter = jest.fn()
    const { result } = renderHook(() => useKeyboardNavigation({ onEnter }))

    const event = { key: 'Tab', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(onEnter).not.toHaveBeenCalled()
    expect(event.preventDefault).not.toHaveBeenCalled()
  })

  it('should not call preventDefault if handler is not provided', () => {
    const { result } = renderHook(() => useKeyboardNavigation({}))

    const event = { key: 'Enter', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    result.current.handleKeyDown(event)

    expect(event.preventDefault).not.toHaveBeenCalled()
  })
})

describe('makeClickableAccessible', () => {
  it('should return correct role', () => {
    const props = makeClickableAccessible(() => {})
    expect(props.role).toBe('button')
  })

  it('should return tabIndex 0', () => {
    const props = makeClickableAccessible(() => {})
    expect(props.tabIndex).toBe(0)
  })

  it('should call onClick when clicked', () => {
    const onClick = jest.fn()
    const props = makeClickableAccessible(onClick)

    props.onClick()

    expect(onClick).toHaveBeenCalled()
  })

  it('should call onClick on Enter key', () => {
    const onClick = jest.fn()
    const props = makeClickableAccessible(onClick)

    const event = { key: 'Enter', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    props.onKeyDown(event)

    expect(onClick).toHaveBeenCalled()
    expect(event.preventDefault).toHaveBeenCalled()
  })

  it('should call onClick on Space key', () => {
    const onClick = jest.fn()
    const props = makeClickableAccessible(onClick)

    const event = { key: ' ', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    props.onKeyDown(event)

    expect(onClick).toHaveBeenCalled()
    expect(event.preventDefault).toHaveBeenCalled()
  })

  it('should not call onClick on other keys', () => {
    const onClick = jest.fn()
    const props = makeClickableAccessible(onClick)

    const event = { key: 'Tab', preventDefault: jest.fn() } as unknown as React.KeyboardEvent
    props.onKeyDown(event)

    expect(onClick).not.toHaveBeenCalled()
    expect(event.preventDefault).not.toHaveBeenCalled()
  })
})
