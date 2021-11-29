const doc = document

const oce = Object.entries

const socket = io()

// socket.emit('request-recommendations', {
//   id
// })

socket.on('new-moodboard-confirmed', (id, name) => {
  console.log(id, name)
})

const fob = obj => {
  for (const [ name, fn ] of oce(obj)) if (typeof fn === 'function') obj[name] = fn.bind(obj)
  return obj
}

let name = ''
let files = []

const { click, focus, blur } = (() => {
  let focussed_data = {
    el: null
  }

  return fob({
    click(uie, target) {
      const { el: focussed_el } = focussed_data

      const this_focussed = focussed_el === uie
      const any_focussed  = focussed_el !== null

      let this_focusable = true

      if (!this_focussed && any_focussed) this.blur(focussed_el)

      switch (uie.getAttribute('type')) {
        case 'submit':
          const modal = doc.querySelector('.modal')
          console.log(name)
          console.log(files)
          socket.emit('create-new-moodboard', {
            name,
            files
          })
          name  = ''
          files = []
          modal.addEventListener('transitionend', e => {
            Array.prototype.forEach.call(doc.querySelectorAll('input'), e => e.value = '')  
          }, { once: true })
          modal.classList.remove('active')
          break
        case 'button':
          this_focusable = false
          const forAttribute = uie.getAttribute('for')
          if (forAttribute) doc.getElementById(forAttribute).classList.toggle('active')
          if (uie.classList.contains('close')) {
            const modal = uie.closest('.modal')
            if (modal) modal.classList.remove('active')
          }
          break
      }

      if (!this_focusable) return

      if (this_focussed) this.activate(uie, target)
      else               this.focus(uie)
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
      let options = {}

      switch (uie.getAttribute('type')) {
        case 'select':
          options = { 'aria-expanded': true }
          break
      }

      focussed_data = { el: uie, options }

      for (const [ attribute, value ] of oce(options)) uie.setAttribute(attribute, value)
    },
    blur(uie) {
      const { el: focussed_el, options: focussed_options } = focussed_data

      if (uie && uie !== focussed_el || !focussed_el) return

      for (const [ attribute, value ] of oce(focussed_options)) focussed_el.setAttribute(attribute, !value)

      focussed_data = { el: null, options: {} }
    }
  })
})()

doc.addEventListener('click', e => {
  const { target } = e
  const uie = target.closest('.uie')

  if (uie) click(uie, target)
  else     blur()
})

function fileToBase64(file) {
  console.log(file)
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const str = reader.result.toString()
      console.log(str)
      resolve(str.substr(str.indexOf(',') + 1))
    }
    reader.onerror = error => reject(error)
    reader.readAsDataURL(file)
  })
}

doc.addEventListener('change', e => {
  const { target } = e
  const type = target.getAttribute('type')
  if (type === 'file') Promise.all(Array.prototype.map.call(e.target.files, fileToBase64)).then(base64Strings => { files = base64Strings })    
  else name = target.value
})