{{/*
Expand the name of the chart.
*/}}
{{- define "dlcs-staff-ui.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "dlcs-staff-ui.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "dlcs-staff-ui.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "dlcs-staff-ui.labels" -}}
helm.sh/chart: {{ include "dlcs-staff-ui.chart" . }}
{{ include "dlcs-staff-ui.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "dlcs-staff-ui.selectorLabels" -}}
app.kubernetes.io/name: {{ include "dlcs-staff-ui.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Deployment Volume Configuration
*/}}
{{- define "dlcs-staff-ui.volumes" -}}
- name: "ohsource"
  persistentVolumeClaim:
    claimName: {{ include "dlcs-staff-ui.fullname" . }}-pvc-ohsource
- name: "ohmasters"
  persistentVolumeClaim:
    claimName: {{ include "dlcs-staff-ui.fullname" . }}-pvc-ohmasters
- name: "ohwowza"
  persistentVolumeClaim:
    claimName: {{ include "dlcs-staff-ui.fullname" . }}-pvc-ohwowza
{{- end }}