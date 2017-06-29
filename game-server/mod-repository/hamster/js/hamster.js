/* Eslint special rule definitions: */
/* global jQuery */

(function ($) {
  /*
  * @description Helper function to toggle an attribute of a dom element.
  *
  * A value for the attribute can be given but is optional. If none given,
  * the attribute will be created empty.
  *
  * @param attribute String
  * @param value String optional
  */
  $.fn.toggleAttr = function (attribute, value) {
    value = value || ''
    if (attribute.length > 0) {
      if (($(this).attr(attribute) !== undefined) && ($(this).attr(attribute) !== value)) {
        $(this).removeAttr(attribute)
      } else {
        $(this).attr(attribute, value)
      }
    }
  }

  /*
  * @description Helper function to retrieve one dict value based on given key.
  *
  * A value for the key is given, for which the value is returned from the
  * given dictionary. Both values are mandatory.
  * If the key is not found, return false.
  *
  * @param key String
  * @param dict Array
  */
  $.fn.getValueFor = function (key, dict) {
    console.log('got call to search "' + key + '" in "' + dict.toString() + '"')
    var result = false
    dict.forEach(function (currentEntry) {
      console.log('Check if "' + currentEntry.key.toString() + '" is the searched key')
      if (currentEntry.key === key.toString()) {
        console.log('Success! Value for key "' + key + '" is "' + currentEntry.value + '"')
        result = currentEntry.value
      }
    })
    if (result === false) {
      console.log('Could not find the key. Returning false.')
    }
    return result
  }

  $.fn.initGUI = function () {
    // init dom elements
    let successAlert = '.alert.alert-success'
    let validationAlert = '.alert.alert-danger.validation'
    let currentUrl = document.location.href.split('?')
    let baseURL = currentUrl[0]
    let tempParams = currentUrl[1].split('&')
    var urlParams = []
    tempParams.forEach(function (currentParam) {
      let tempParam = currentParam.split('=')
      let tempKey = tempParam[0].toString()
      let tempValue = tempParam[1].toString()
      urlParams.push({
        key: tempKey,
        value: tempValue
      })
    }, this)
    var iterationCounter = 0
    let mainForm = {}
    mainForm.form = $('form.mod-submit')
    mainForm.addInputButton = mainForm.form + $('.add-file-input')

    function handleTogglesWithValidationErrors () {
      if ($('.toggle label.validation-error').length <= 0) {
        $('.toggle').hide()
      }
    }

    function handleAlerts () {
      // show different alerts and scroll to top if one is shown.
      // Success alerts stay while error alerts are hidden after some time.
      if ($(validationAlert).length > 0 || $(successAlert).length > 0 && $().getValueFor('submit', urlParams) === 'success') {
        // Assume validation error has happened and alert should be shown
        $('body').animate({ scrollTop: 0 }, 'slow', 'easeOutSine')
        $('.alert').removeClass('vishidden')
      }
      // Scroll to top if success alert is shown
      if ($(successAlert + ':visible')) {
        $('body').animate({ scrollTop: 0 }, 'slow', 'easeOutSine')
      }
    }

    function replaceEditURL (placeholder) {
      // replaces the given placeholder in the success alert after mod submission with hash
      // from url parameter.
      let modHash = $().getValueFor('hash', urlParams)
      let modEditURL = baseURL + 'edit_mod?securekey=' + modHash
      var text = $(successAlert).text()
      $(successAlert).text(text.replace(placeholder, modEditURL))
    }

    function handlePackageName () {
      // show 'package_name' input field only if 'package_bool' checkbox is checked.
      // Maybe generalize this behaviour later for the pybottle webform framework.
      $('#package_bool').on('click', function () {
        let packageNameBool = $('#package_bool')
        let packageNameInputContainer = $('#package_bool').parents('.form-group').siblings('.toggle')
        let packageNameInput = packageNameInputContainer.find('input')
        let originalID = packageNameInput.prop('id')

        if (packageNameBool.prop('checked') === true) {
          packageNameInputContainer.fadeIn()
          packageNameInput.prop({
            'id': originalID + '_req',
            'name': originalID + '_req'
          })
        } else {
          packageNameInputContainer.fadeOut()
          packageNameInput.prop({
            'id': originalID,
            'name': originalID
          })
        }
      })
    }

    function cloneFormInputElementButton (buttonElement) {
      // Based on two element ids, a source and a target, clone the source input element
      // and append it at the last position after the target element and all previously
      // cloned elements. To distinguish between cloned elements in form processing,
      // the id and name of each cloned input is appended with a running number.
      // Also clone associated elements of the source element.
      $(buttonElement).on('click', function () {
        // get element selectors from button data attributes
        let targetElement = $(buttonElement).attr('data-target-element')
        let sourceElement = $(buttonElement).attr('data-source-element')
        let assocElement = $(sourceElement).attr('data-associated-with')
        // let assocElement = $('[data-associated-with="' + sourceElement + '"]')
        let hasAssocElement = $(assocElement).length > 0
        iterationCounter++
        // generate new ids/names of the new element
        let newElementID = $(sourceElement).prop('name') + '_' + iterationCounter.toString()
        let newAssocElementID = $(assocElement).prop('name') + '_' + iterationCounter.toString()
        // clone new element and change its attributes
        let newElement = $(sourceElement).clone().prop({
          'id': newElementID,
          'name': newElementID,
          'value': '',
          // 'value': newElementID, // This will print the element-ID into the element, helping to understand sorting issues
          'data-associated-with': newAssocElementID
        })
        // clone the associated element, if existing, and change its attributes
        if (hasAssocElement) {
          var newAssocElement = $(assocElement).clone().prop({
            'id': newAssocElementID,
            'name': newAssocElementID,
            'value': '',
            // 'value': newAssocElementID, // This will print the element-ID into the element, helping to understand sorting issues
            'data-associated-with': newElementID
          })
        }
        var target = ''
        if (hasAssocElement) {
          target = assocElement
        } else {
          target = targetElement
        }
        // If source element has been cloned at least once, insert after the last cloned
        // element instead of the original target element
        if (iterationCounter >= 2) {
          if (hasAssocElement) {
            target = '#' + $(assocElement).prop('name') + '_' + (iterationCounter - 1).toString()
          } else {
            target = '#' + $(sourceElement).prop('name') + '_' + (iterationCounter - 1).toString()
          }
        }
        // Insert cloned element/s.
        if (hasAssocElement) {
          newAssocElement.insertAfter($(target))
        }
        newElement.insertAfter($(target))
      })
    }

    // Dynamically add mod-change URL to success-alert
    replaceEditURL('{MOD_EDIT_URL}')
    // handle the showing and fading of alerts
    handleAlerts()
    // if validation error happened for one bools associated element, don't hide it
    handleTogglesWithValidationErrors()
    // if 'package' checkbox clicked, show associated input element
    handlePackageName()
    // handle form input element clone buttons
    let cloneInputButtons = $('.clone-input')
    if (cloneInputButtons.length > 1) {
      for (var button in cloneInputButtons) {
        cloneFormInputElementButton(button)
      }
    } else {
      cloneFormInputElementButton(cloneInputButtons)
    }
  }
}(jQuery))
console.log('GUI module initialized')
