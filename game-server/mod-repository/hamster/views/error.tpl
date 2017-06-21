% include('header')

% error_header = str(error_type+'_header')
% error_description = str(error_type+'_description')

<div class="center-block bg-danger generic-error">
  <h1 class="text-danger">Dammit: {{strings[error_header]}}</h1>
  <p>{{strings[error_description]}}</p>
</div>

% include('footer')
