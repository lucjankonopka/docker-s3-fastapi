{{- define "docker-s3-fastapi.name" -}}
docker-s3-fastapi
{{- end }}

{{- define "docker-s3-fastapi.fullname" -}}
{{ include "docker-s3-fastapi.name" . }}
{{- end }}