# {{manifest.name}}

{{manifest.description}}

## Website

{{manifest.source}}

## Installation

## Usage Notes

The {{manifest.label}} gear is executed by ensuring the following required inputs and configuration parameters are provided. Additional optional inputs are indicated below.

{{#manifest.has_inputs}}
### Inputs

{{/manifest.has_inputs}}
{{#manifest.inputs_list}}
* **{{name}}** {{#optional}} (optional){{/optional}}{{^optional}}(required){{/optional}}: {{description}}
{{/manifest.inputs_list}}

{{#manifest.has_configs}}
### Parameters

{{/manifest.has_configs}}
{{#manifest.config_list}}
* **{{name}}** {{#optional}} (optional){{/optional}}{{^optional}}(required){{/optional}}: {{description}} {{#default_val}} (Default {{val}}).{{/default_val}}
{{/manifest.config_list}}