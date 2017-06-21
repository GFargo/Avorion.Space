% setdefault('originalInput', '')
% setdefault('invalidation_field', '')
% setdefault('invalidation_cause', '')
% setdefault('value', '')
% setdefault('placeholder', '')
% setdefault('association', '')
% global tabindex
% tabindex = 0
% global required_flag
% required_flag = ''

% def show_notification(urgency, title, message, classes=None):
<div class="alert alert-{{urgency}}
  %   if classes is not None:
  %     for cssClass in classes:
   {{cssClass}}
  %     end
  %   end
" role="alert">
  <p><b>{{title}}</b> {{message}}</p>
</div>
% end

% include('header')

% if invalidation_field:
%   show_notification('danger', 'Input error!', 'Please check the form, it seems there was an error.', ['validation', 'vishidden', 'visfade'])
% else:
%   show_notification('success', 'Mod submitted!', 'Your mod will be available via Avorion Mod Manager within the next 5-10 minutes.', ['vishidden', 'visfade'])
% end

<!-- Input Element begin -->
% def render_input_element(element, type, mandatory_flag=False):
  % element_id = element+'_'+type
  % tabindex = tabindex + 1

  % # This adds a string fragment to the element ID because apart from the name of the input
  % # element, nothing is transmitted and using invisible form elements for this sucks.
  % if mandatory_flag:
  %   element_id = element_id + '_req'
  %   global required_flag
  %   required_flag = 'required'
  % end

  % # To set a boolean input to checked state if it was submitted checked, we do this.
  % # Please note that a type="checkbox" is seen as value "on" on python serverside after submit,
  % # so this is why we need to translate forth and back.
  % bool_checked = ''
  % if invalidation_field and type == 'bool':
  %   if originalInput.get(element_id) == 'on':
  %     bool_checked = 'checked'
  %   end
  % end

  % # The reasons for a failed validation are given as two ordered arrays where each entry of one
  % # array refers to the element at the same position in the other array. One gives reasons (causes)
  % # and the other element IDs. This resolves this and gives the validation error message for the
  % # current element.
  % try:
    % cause_index = invalidation_field.index(element_id)
    % # print('cause_index is '+str(cause_index))
    % validation_error_message = 'validation_error_'+invalidation_cause[cause_index]
  % except Exception, e:
    % print(str(e))
    % pass
  % end

<div class="form-group
  % if element_id in invalidation_field:
  has-error
  % end
  % if type == 'file':
  file
  % end
  % if element == 'package_name':
  package_name toggle
  % end
  ">
  <div class="col-sm-4">
    <label for="{{element_id}}">{{strings['label_'+element]}}</label>
    % if 'hint_'+element in strings:
      <p class="help-block">{{strings['hint_'+element]}}</p>
    % end
  </div>

  <div class="col-sm-8">
  <!-- Start Text, Version, URL input definition -->
  % if type in ['text', 'version', 'url', 'file']:
    % placeholder = ''
    % value = ''
    % association = ''
    % if 'gamepath' in element and strings['placeholder_'+element]:
    %   placeholder = strings['placeholder_'+element]
    % end
    % if invalidation_field:
    %   value = originalInput.get(element_id)
    % end
    % if type == 'file':
    %   association = 'data-associated-with=#gamepath_text'
    % end
    <input tabindex="{{tabindex}}" type="text" name="{{element_id}}" id="{{element_id}}" class="form-control" autofocus="" placeholder="{{placeholder}}" value="{{value}}" {{association}}>

    <!-- In case of file input element add the additional "relative_path" input field, associated with the file -->
    % if type == 'file':
    %   tabindex = tabindex + 1
    %   assoc_element_id = 'gamepath_text'
    %   if invalidation_field:
    %     value = 'value=' + originalInput.get(assoc_element_id)
    %   end
    <input tabindex="{{tabindex}}" type="text" name="{{assoc_element_id}}" id="{{assoc_element_id}}" data-associated-with="#{{element_id}}" class="form-control" autofocus="" {{value}}>
    % end
    
    % # <!-- If additional input file and associated text elements where created by user before the submit, create them again on the fly -->
    % if invalidation_field and type == 'file':
    %   for attribute in originalInput:
    %     if 'file_' in attribute and any(char.isdigit() for char in attribute):
    % #     <!-- Bingo! We found an element that the user created. Now we recreate it and also the associated gamepath element based on the index at the end of the first element. -->
    %       element_index = attribute.rsplit('_', 1)[1]
    %       assoc_element_id = 'gamepath_text_'+str(element_index)
    %       association = 'data-associated-with=#gamepath_text_'+str(element_index)
    %       tabindex = tabindex + 1
            % print('Creating file element first')
            <input tabindex="{{tabindex}}" type="text" name="{{element_id}}" id="{{element_id}}" class="form-control" autofocus="" value="{{originalInput.get(attribute)}}" placeholder="{{placeholder}}" {{association}}>
            % print('Now creating associated gamepath element')
    %       tabindex = tabindex + 1
            <input tabindex="{{tabindex}}" type="text" name="{{assoc_element_id}}" id="{{assoc_element_id}}" data-associated-with="#{{element_id}}" class="form-control" autofocus="" value="{{originalInput.get(assoc_element_id)}}">
    %     end
    %   end
    % end


    <!-- In case of file input element add "add another input" button at bottom -->
    % if type == 'file':
    %   global tabindex
    %   tabindex = tabindex + 1
        <input class="btn btn-default clone-input btn-block" value="Add another one" data-source-element="#file_file_req" data-target-element="#file_file_req">
    % end

  <!--  Start Bool input definition -->
  % elif type == 'bool':
    <input tabindex="{{tabindex}}" type="checkbox" name="{{element_id}}" id="{{element_id}}" {{bool_checked}}>
  % end

  </div>
  % if element_id in invalidation_field:
    <label for="{{element_id}}" class="control-label validation-error col-sm-8 pull-right text-left">{{strings[validation_error_message]}}</label>
  % end

</div>
% end
<!-- End of input element -->

<form class="mod-submit form-horizontal" method="post">
  <h2 class="mod-submit-head">{{strings['header']}}</h2>
  <p>{{strings['description']}}</p>

  % ### Definition of input elements follows this scheme:
  % ### id_of_element : string, input_type_of_element : string, is_mandatory : bool
  % render_input_element('modname', 'text', True)
  % render_input_element('description', 'text', True)
  % render_input_element('author', 'text', True)
  % render_input_element('mod_version', 'version')
  % render_input_element('game_version', 'version')
  % render_input_element('url', 'url')
  % render_input_element('package', 'bool')
  % render_input_element('package_name', 'text')
  % render_input_element('file', 'file', True)

  <button class="btn btn-lg btn-primary btn-block" type="submit">{{strings['label_submit']}}</button>
</form>

% include('footer')
