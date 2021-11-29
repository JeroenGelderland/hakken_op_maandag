const doc = document

const oce = Object.entries

const fob = obj => {
  for (const [ name, fn ] of oce(obj)) if (typeof fn === 'function') obj[name] = fn.bind(obj)
  return obj
}

const { click, focus, blur } = (() => {
  let focussedData = {
    el: null
  }

  return fob({
    click(uie, target) {
      const { el: focussedEl } = focussedData
      const focussed  = focussedEl !== null
      const focussing = focussedEl !== uie
      if (focussing) {
        if (focussed) this.blur(focussedEl)
        this.focus(uie)
      } else {
        this.activate(uie, target)
      }
    },
    activate(uie, target) {
      switch (uie.getAttribute('type')) {
        case 'select':
          if (target.tagName === 'BUTTON') {
            const result = Array.prototype.find.call(uie.children, el => el.classList.contains('result'))
            result.innerHTML = target.innerText
          }
          blur(uie)
          break
      }
    },
    focus(uie) {
      let options

      switch (uie.getAttribute('type')) {
        case 'select':
          options = { 'aria-expanded': true }
          break
      }

      focussedData = { el: uie, options }

      for (const [ attribute, value ] of oce(options)) uie.setAttribute(attribute, value)
    },
    blur(uie) {
      const { el: focussedEl, options: focussedOptions } = focussedData

      if (uie && uie !== focussedEl) return

      for (const [ attribute, value ] of oce(focussedOptions)) focussedEl.setAttribute(attribute, !value)

      focussedData = { el: null }
    }
  })
})()

doc.addEventListener('click', e => {
  const { target } = e
  const uie = target.closest('.uie')

  if (uie) click(uie, target)
  else     blur()
})