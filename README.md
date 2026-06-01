Hi, I'm Peter 👋

I have authored and/or currently maintain hundreds of open source libraries, including many you might use (as a developer or a consumer of the internet).

I recently worked on the Go project for dependency license scanning [Apache SkyWalking Eyes](https://github.com/apache/skywalking-eyes), where I integrated bundler and gemspec (Ruby) compatibility,  added ASF Category A and B license checks, FSF Free/Libre checks, and OSI Approved checks (all configurable). Learn how to use it in as a [GitHub Action](https://dev.to/galtzo/how-to-check-license-compatibility-41h0) in your project.

[demo]: https://pboling.github.io/yacs/
[demo-img]: https://img.shields.io/badge/Live-Demo-blue

<details>
    <summary>👣 How will my projects approach the September 2025 hostile takeover of RubyGems? 🚑️</summary>

I've summarized my thoughts in [this blog post](https://dev.to/galtzo/hostile-takeover-of-rubygems-my-thoughts-5hlo).

</details>

[draper-security]: https://joel.drapper.me/p/ruby-central-security-measures/
[draper-takeover]: https://joel.drapper.me/p/ruby-central-takeover/
[draper-lies]: https://joel.drapper.me/p/ruby-central-fact-check/
[draper-theft]: https://joel.drapper.me/p/ruby-central/
[gem-coop]: https://gem.coop
[martin-ann]: https://martinemde.com/2025/10/05/announcing-gem-coop.html

I maintain the following RubyGems:

- appraisal-rb / appraisal2 - [![Downloads Rank 🐙:appraisal-rb/appraisal2](https://img.shields.io/gem/rd/appraisal2.svg)](https://bestgems.org/gems/appraisal2)
- Dynamoid / dynamoid - [![Downloads Rank 🐙:Dynamoid/dynamoid](https://img.shields.io/gem/rd/dynamoid.svg)](https://bestgems.org/gems/dynamoid)
- galtzo-floss / flag_shih_tzu - [![Downloads Rank 🐙:galtzo-floss/flag_shih_tzu](https://img.shields.io/gem/rd/flag_shih_tzu.svg)](https://bestgems.org/gems/flag_shih_tzu)
- galtzo-floss / sanitize_email - [![Downloads Rank 🐙:galtzo-floss/sanitize_email](https://img.shields.io/gem/rd/sanitize_email.svg)](https://bestgems.org/gems/sanitize_email)
- structuredmerge / ruby / tree_haver - [![Downloads Rank 🐙:structuredmerge/ruby/tree_haver](https://img.shields.io/gem/rd/tree_haver.svg)](https://bestgems.org/gems/tree_haver)
- structuredmerge / ruby / ast-merge - [![Downloads Rank 🐙:structuredmerge/ruby/ast-merge](https://img.shields.io/gem/rd/ast-merge.svg)](https://bestgems.org/gems/ast-merge)
- omniauth / omniauth-jwt - [![Downloads Rank 🐙:omniauth/omniauth-jwt](https://img.shields.io/gem/rd/omniauth-jwt.svg)](https://bestgems.org/gems/omniauth-jwt)
- omniauth / omniauth-identity - [![Downloads Rank 🐙:omniauth/omniauth-identity](https://img.shields.io/gem/rd/omniauth-identity.svg)](https://bestgems.org/gems/omniauth-identity)
- omniauth / omniauth-ldap - [![Downloads Rank 🐙:omniauth/omniauth-ldap](https://img.shields.io/gem/rd/omniauth-ldap.svg)](https://bestgems.org/gems/omniauth-ldap)
- rdp / os - [![Downloads Rank 🐙:rdp/os](https://img.shields.io/gem/rd/os.svg)](https://bestgems.org/gems/os)
- ruby-oauth / auth-sanitizer - [![Downloads Rank 🐙:ruby-oauth/auth-sanitizer](https://img.shields.io/gem/rd/auth-sanitizer.svg)](https://bestgems.org/gems/auth-sanitizer)
- ruby-oauth / oauth - [![Downloads Rank 🐙:ruby-oauth/oauth](https://img.shields.io/gem/rd/oauth.svg)](https://bestgems.org/gems/oauth)
- ruby-oauth / oauth2 - [![Downloads Rank 🐙:ruby-oauth/oauth2](https://img.shields.io/gem/rd/oauth2.svg)](https://bestgems.org/gems/oauth2)
- ruby-oauth / version_gem - [![Downloads Rank 🐙:ruby-oauth/version_gem](https://img.shields.io/gem/rd/version_gem.svg)](https://bestgems.org/gems/version_gem)
- ruby-openid / omniauth-openid - [![Downloads Rank 🐙:ruby-openid/omniauth-openid](https://img.shields.io/gem/rd/omniauth-openid.svg)](https://bestgems.org/gems/omniauth-openid)
- ruby-openid / rack-openid - [![Downloads Rank 🐙:ruby-openid/rack-openid](https://img.shields.io/gem/rd/rack-openid.svg)](https://bestgems.org/gems/rack-openid)
- ruby-openid / ruby-openid - [![Downloads Rank 🐙:ruby-openid/ruby-openid](https://img.shields.io/gem/rd/ruby-openid.svg)](https://bestgems.org/gems/ruby-openid)
- many ast-parsing, benchmarking, rails, resque, rspec, rubocop plugins & more... (in details below)

<details>
  <summary>ast-parsing libraries</summary>

### The `*-merge` Gem Family

The `*-merge` gem family provides intelligent, AST-based merging for various file formats. At the foundation is [tree_haver][tree_haver], which provides a unified cross-Ruby parsing API that works seamlessly across MRI, JRuby, and TruffleRuby.

| Gem                                      |                                                         Version / CI                                                         | Language<br>/ Format | Parser Backend(s)                                                                                     | Description                                                                      |
|------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------:|----------------------|-------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| [tree_haver][tree_haver]                 |                 [![Version][tree_haver-gem-i]][tree_haver-gem] <br/> [![CI][tree_haver-ci-i]][tree_haver-ci]                 | Multi                | Supported Backends: MRI C, Rust, FFI, Java, Prism, Psych, Commonmarker, Markly, Citrus, Parslet       | **Foundation**: Cross-Ruby adapter for parsing libraries (like Faraday for HTTP) |
| [ast-merge][ast-merge]                   |                   [![Version][ast-merge-gem-i]][ast-merge-gem] <br/> [![CI][ast-merge-ci-i]][ast-merge-ci]                   | Text                 | internal                                                                                              | **Infrastructure**: Shared base classes and merge logic for all `*-merge` gems   |
| [bash-merge][bash-merge]                 |                 [![Version][bash-merge-gem-i]][bash-merge-gem] <br/> [![CI][bash-merge-ci-i]][bash-merge-ci]                 | Bash                 | [tree-sitter-bash][ts-bash] (via tree_haver)                                                          | Smart merge for Bash scripts                                                     |
| [commonmarker-merge][commonmarker-merge] | [![Version][commonmarker-merge-gem-i]][commonmarker-merge-gem] <br/> [![CI][commonmarker-merge-ci-i]][commonmarker-merge-ci] | Markdown             | [Commonmarker][commonmarker] (via tree_haver)                                                         | Smart merge for Markdown (CommonMark via comrak Rust)                            |
| [dotenv-merge][dotenv-merge]             |             [![Version][dotenv-merge-gem-i]][dotenv-merge-gem] <br/> [![CI][dotenv-merge-ci-i]][dotenv-merge-ci]             | Dotenv               | internal                                                                                              | Smart merge for `.env` files                                                     |
| [json-merge][json-merge]                 |                 [![Version][json-merge-gem-i]][json-merge-gem] <br/> [![CI][json-merge-ci-i]][json-merge-ci]                 | JSON                 | [tree-sitter-json][ts-json] (via tree_haver)                                                          | Smart merge for JSON files                                                       |
| [jsonc-merge][jsonc-merge]               |               [![Version][jsonc-merge-gem-i]][jsonc-merge-gem] <br/> [![CI][jsonc-merge-ci-i]][jsonc-merge-ci]               | JSONC                | [tree-sitter-jsonc][ts-jsonc] (via tree_haver)                                                        | ⚠️ Proof of concept; Smart merge for JSON with Comments                          |
| [markdown-merge][markdown-merge]         |         [![Version][markdown-merge-gem-i]][markdown-merge-gem] <br/> [![CI][markdown-merge-ci-i]][markdown-merge-ci]         | Markdown             | [Commonmarker][commonmarker] / [Markly][markly] (via tree_haver), [Parslet][parslet]                  | **Foundation**: Shared base for Markdown mergers with inner code block merging   |
| [markly-merge][markly-merge]             |             [![Version][markly-merge-gem-i]][markly-merge-gem] <br/> [![CI][markly-merge-ci-i]][markly-merge-ci]             | Markdown             | [Markly][markly] (via tree_haver)                                                                     | Smart merge for Markdown (CommonMark via cmark-gfm C)                            |
| [prism-merge][prism-merge]               |               [![Version][prism-merge-gem-i]][prism-merge-gem] <br/> [![CI][prism-merge-ci-i]][prism-merge-ci]               | Ruby                 | [Prism][prism] (`prism` std lib gem)                                                                  | Smart merge for Ruby source files                                                |
| [psych-merge][psych-merge]               |               [![Version][psych-merge-gem-i]][psych-merge-gem] <br/> [![CI][psych-merge-ci-i]][psych-merge-ci]               | YAML                 | [Psych][psych] (`psych` std lib gem)                                                                  | Smart merge for YAML files                                                       |
| [rbs-merge][rbs-merge]                   |                   [![Version][rbs-merge-gem-i]][rbs-merge-gem] <br/> [![CI][rbs-merge-ci-i]][rbs-merge-ci]                   | RBS                  | [tree-sitter-bash][ts-rbs] (via tree_haver), [RBS][rbs] (`rbs` std lib gem)                           | Smart merge for Ruby type signatures                                             |
| [toml-merge][toml-merge]                 |                 [![Version][toml-merge-gem-i]][toml-merge-gem] <br/> [![CI][toml-merge-ci-i]][toml-merge-ci]                 | TOML                 | [Parslet + toml][toml], [Citrus + toml-rb][toml-rb], [tree-sitter-toml][ts-toml] (all via tree_haver) | Smart merge for TOML files                                                       |

#### Backend Platform Compatibility

tree_haver supports multiple parsing backends, but not all backends work on all Ruby platforms:

| Platform 👉️<br> TreeHaver Backend 👇️          | MRI | JRuby | TruffleRuby | Notes                                                                      |
|-------------------------------------------------|:---:|:-----:|:-----------:|----------------------------------------------------------------------------|
| **MRI** ([ruby_tree_sitter][ruby_tree_sitter])  |  ✅  |   ❌   |      ❌      | C extension, MRI only                                                      |
| **Rust** ([tree_stump][tree_stump])             |  ✅  |   ❌   |      ❌      | Rust extension via magnus/rb-sys, MRI only                                 |
| **FFI** ([ffi][ffi])                            |  ✅  |   ✅   |      ❌      | TruffleRuby's FFI doesn't support `STRUCT_BY_VALUE`                        |
| **Java** ([jtreesitter][jtreesitter])           |  ❌  |   ✅   |      ❌      | JRuby only, requires grammar JARs                                          |
| **Prism** ([prism][prism])                      |  ✅  |   ✅   |      ✅      | Ruby parsing, stdlib in Ruby 3.4+                                          |
| **Psych** ([psych][psych])                      |  ✅  |   ✅   |      ✅      | YAML parsing, stdlib                                                       |
| **Citrus** ([citrus][citrus])                   |  ✅  |   ✅   |      ✅      | Pure Ruby PEG parser, no native dependencies                               |
| **Parslet** ([parslet][parslet])                |  ✅  |   ✅   |      ✅      | Pure Ruby PEG parser, no native dependencies                               |
| **Commonmarker** ([commonmarker][commonmarker]) |  ✅  |   ❌   |      ❓      | Rust extension for Markdown (via [commonmarker-merge][commonmarker-merge]) |
| **Markly** ([markly][markly])                   |  ✅  |   ❌   |      ❓      | C extension for Markdown  (via [markly-merge][markly-merge])               |

**Legend**: ✅ = Works, ❌ = Does not work, ❓ = Untested

**Why some backends don't work on certain platforms**:

- **JRuby**: Runs on the JVM; cannot load native C/Rust extensions (`.so` files)
- **TruffleRuby**: Has C API emulation via Sulong/LLVM, but it doesn't expose all MRI internals that native extensions require (e.g., `RBasic.flags`, `rb_gc_writebarrier`)
- **FFI on TruffleRuby**: TruffleRuby's FFI implementation doesn't support returning structs by value, which tree-sitter's C API requires

**Example implementations** for the gem templating use case:

| Gem                      | Purpose         | Description                                   |
|--------------------------|-----------------|-----------------------------------------------|
| [kettle-dev][kettle-dev] | Gem Development | Gem templating tool using `*-merge` gems      |
| [kettle-jem][kettle-jem] | Gem Templating  | Gem template library with smart merge support |

[tree_haver]: https://github.com/kettle-rb/tree_haver
[ast-merge]: https://github.com/kettle-rb/ast-merge
[prism-merge]: https://github.com/kettle-rb/prism-merge
[psych-merge]: https://github.com/kettle-rb/psych-merge
[json-merge]: https://github.com/kettle-rb/json-merge
[jsonc-merge]: https://github.com/kettle-rb/jsonc-merge
[bash-merge]: https://github.com/kettle-rb/bash-merge
[rbs-merge]: https://github.com/kettle-rb/rbs-merge
[dotenv-merge]: https://github.com/kettle-rb/dotenv-merge
[toml-merge]: https://github.com/kettle-rb/toml-merge
[markdown-merge]: https://github.com/kettle-rb/markdown-merge
[markly-merge]: https://github.com/kettle-rb/markly-merge
[commonmarker-merge]: https://github.com/kettle-rb/commonmarker-merge
[kettle-dev]: https://github.com/kettle-rb/kettle-dev
[kettle-jem]: https://github.com/kettle-rb/kettle-jem
[tree_haver-gem]: https://bestgems.org/gems/tree_haver
[ast-merge-gem]: https://bestgems.org/gems/ast-merge
[prism-merge-gem]: https://bestgems.org/gems/prism-merge
[psych-merge-gem]: https://bestgems.org/gems/psych-merge
[json-merge-gem]: https://bestgems.org/gems/json-merge
[jsonc-merge-gem]: https://bestgems.org/gems/jsonc-merge
[bash-merge-gem]: https://bestgems.org/gems/bash-merge
[rbs-merge-gem]: https://bestgems.org/gems/rbs-merge
[dotenv-merge-gem]: https://bestgems.org/gems/dotenv-merge
[toml-merge-gem]: https://bestgems.org/gems/toml-merge
[markdown-merge-gem]: https://bestgems.org/gems/markdown-merge
[markly-merge-gem]: https://bestgems.org/gems/markly-merge
[commonmarker-merge-gem]: https://bestgems.org/gems/commonmarker-merge
[kettle-dev-gem]: https://bestgems.org/gems/kettle-dev
[kettle-jem-gem]: https://bestgems.org/gems/kettle-jem
[tree_haver-gem-i]: https://img.shields.io/gem/v/tree_haver.svg
[ast-merge-gem-i]: https://img.shields.io/gem/v/ast-merge.svg
[prism-merge-gem-i]: https://img.shields.io/gem/v/prism-merge.svg
[psych-merge-gem-i]: https://img.shields.io/gem/v/psych-merge.svg
[json-merge-gem-i]: https://img.shields.io/gem/v/json-merge.svg
[jsonc-merge-gem-i]: https://img.shields.io/gem/v/jsonc-merge.svg
[bash-merge-gem-i]: https://img.shields.io/gem/v/bash-merge.svg
[rbs-merge-gem-i]: https://img.shields.io/gem/v/rbs-merge.svg
[dotenv-merge-gem-i]: https://img.shields.io/gem/v/dotenv-merge.svg
[toml-merge-gem-i]: https://img.shields.io/gem/v/toml-merge.svg
[markdown-merge-gem-i]: https://img.shields.io/gem/v/markdown-merge.svg
[markly-merge-gem-i]: https://img.shields.io/gem/v/markly-merge.svg
[commonmarker-merge-gem-i]: https://img.shields.io/gem/v/commonmarker-merge.svg
[kettle-dev-gem-i]: https://img.shields.io/gem/v/kettle-dev.svg
[kettle-jem-gem-i]: https://img.shields.io/gem/v/kettle-jem.svg
[tree_haver-ci-i]: https://github.com/kettle-rb/tree_haver/actions/workflows/current.yml/badge.svg
[ast-merge-ci-i]: https://github.com/kettle-rb/ast-merge/actions/workflows/current.yml/badge.svg
[prism-merge-ci-i]: https://github.com/kettle-rb/prism-merge/actions/workflows/current.yml/badge.svg
[psych-merge-ci-i]: https://github.com/kettle-rb/psych-merge/actions/workflows/current.yml/badge.svg
[json-merge-ci-i]: https://github.com/kettle-rb/json-merge/actions/workflows/current.yml/badge.svg
[jsonc-merge-ci-i]: https://github.com/kettle-rb/jsonc-merge/actions/workflows/current.yml/badge.svg
[bash-merge-ci-i]: https://github.com/kettle-rb/bash-merge/actions/workflows/current.yml/badge.svg
[rbs-merge-ci-i]: https://github.com/kettle-rb/rbs-merge/actions/workflows/current.yml/badge.svg
[dotenv-merge-ci-i]: https://github.com/kettle-rb/dotenv-merge/actions/workflows/current.yml/badge.svg
[toml-merge-ci-i]: https://github.com/kettle-rb/toml-merge/actions/workflows/current.yml/badge.svg
[markdown-merge-ci-i]: https://github.com/kettle-rb/markdown-merge/actions/workflows/current.yml/badge.svg
[markly-merge-ci-i]: https://github.com/kettle-rb/markly-merge/actions/workflows/current.yml/badge.svg
[commonmarker-merge-ci-i]: https://github.com/kettle-rb/commonmarker-merge/actions/workflows/current.yml/badge.svg
[kettle-dev-ci-i]: https://github.com/kettle-rb/kettle-dev/actions/workflows/current.yml/badge.svg
[kettle-jem-ci-i]: https://github.com/kettle-rb/kettle-jem/actions/workflows/current.yml/badge.svg
[tree_haver-ci]: https://github.com/kettle-rb/tree_haver/actions/workflows/current.yml
[ast-merge-ci]: https://github.com/kettle-rb/ast-merge/actions/workflows/current.yml
[prism-merge-ci]: https://github.com/kettle-rb/prism-merge/actions/workflows/current.yml
[psych-merge-ci]: https://github.com/kettle-rb/psych-merge/actions/workflows/current.yml
[json-merge-ci]: https://github.com/kettle-rb/json-merge/actions/workflows/current.yml
[jsonc-merge-ci]: https://github.com/kettle-rb/jsonc-merge/actions/workflows/current.yml
[bash-merge-ci]: https://github.com/kettle-rb/bash-merge/actions/workflows/current.yml
[rbs-merge-ci]: https://github.com/kettle-rb/rbs-merge/actions/workflows/current.yml
[dotenv-merge-ci]: https://github.com/kettle-rb/dotenv-merge/actions/workflows/current.yml
[toml-merge-ci]: https://github.com/kettle-rb/toml-merge/actions/workflows/current.yml
[markdown-merge-ci]: https://github.com/kettle-rb/markdown-merge/actions/workflows/current.yml
[markly-merge-ci]: https://github.com/kettle-rb/markly-merge/actions/workflows/current.yml
[commonmarker-merge-ci]: https://github.com/kettle-rb/commonmarker-merge/actions/workflows/current.yml
[kettle-dev-ci]: https://github.com/kettle-rb/kettle-dev/actions/workflows/current.yml
[kettle-jem-ci]: https://github.com/kettle-rb/kettle-jem/actions/workflows/current.yml
[prism]: https://github.com/ruby/prism
[psych]: https://github.com/ruby/psych
[ffi]: https://github.com/ffi/ffi
[ts-json]: https://github.com/tree-sitter/tree-sitter-json
[ts-jsonc]: https://gitlab.com/WhyNotHugo/tree-sitter-jsonc
[ts-bash]: https://github.com/tree-sitter/tree-sitter-bash
[ts-rbs]: https://github.com/joker1007/tree-sitter-rbs
[ts-toml]: https://github.com/tree-sitter-grammars/tree-sitter-toml
[dotenv]: https://github.com/bkeepers/dotenv
[rbs]: https://github.com/ruby/rbs
[toml-rb]: https://github.com/emancu/toml-rb
[toml]: https://github.com/jm/toml
[markly]: https://github.com/ioquatix/markly
[commonmarker]: https://github.com/gjtorikian/commonmarker
[ruby_tree_sitter]: https://github.com/Faveod/ruby-tree-sitter
[tree_stump]: https://github.com/joker1007/tree_stump
[jtreesitter]: https://central.sonatype.com/artifact/io.github.tree-sitter/jtreesitter
[citrus]: https://github.com/mjackson/citrus
[parslet]: https://github.com/kschiess/parslet

</details>

<details>
  <summary>benchmarking libraries</summary>

- galtzo-floss / debug_logging - [![Downloads Rank 🐙:galtzo-floss/debug_logging](https://img.shields.io/gem/rd/debug_logging.svg)](https://bestgems.org/gems/debug_logging)
- galtzo-floss / gem_bench - [![Downloads Rank 🐙:galtzo-floss/gem_bench](https://img.shields.io/gem/rd/gem_bench.svg)](https://bestgems.org/gems/gem_bench)
- galtzo-floss / react-rails-benchmark_renderer - [![Downloads Rank 🐙:galtzo-floss/react-rails-benchmark_renderer](https://img.shields.io/gem/rd/react-rails-benchmark_renderer.svg)](https://bestgems.org/gems/react-rails-benchmark_renderer)
- galtzo-floss / require_bench - [![Downloads Rank 🐙:galtzo-floss/require_bench](https://img.shields.io/gem/rd/require_bench.svg)](https://bestgems.org/gems/require_bench)

</details>

<details>
  <summary>rails plugins</summary>

- galtzo-floss / active_security - [![Downloads Rank 🐙:galtzo-floss/active_security](https://img.shields.io/gem/rd/active_security.svg)](https://bestgems.org/gems/active_security)
- galtzo-floss / activerecord-transactionable - [![Downloads Rank 🐙:galtzo-floss/activerecord-transactionable](https://img.shields.io/gem/rd/activerecord-transactionable.svg)](https://bestgems.org/gems/activerecord-transactionable)
- galtzo-floss / activesupport-broadcast_logger - [![Downloads Rank 🐙:galtzo-floss/activesupport-broadcast_logger](https://img.shields.io/gem/rd/activesupport-broadcast_logger.svg)](https://bestgems.org/gems/activesupport-broadcast_logger)
- galtzo-floss / activesupport-logger - [![Downloads Rank 🐙:galtzo-floss/activesupport-logger](https://img.shields.io/gem/rd/activesupport-logger.svg)](https://bestgems.org/gems/activesupport-logger)
- galtzo-floss / activesupport-tagged_logging - [![Downloads Rank 🐙:galtzo-floss/activesupport-tagged_logging](https://img.shields.io/gem/rd/activesupport-tagged_logging.svg)](https://bestgems.org/gems/activesupport-tagged_logging)
- galtzo-floss / debug_logging - [![Downloads Rank 🐙:galtzo-floss/debug_logging](https://img.shields.io/gem/rd/debug_logging.svg)](https://bestgems.org/gems/debug_logging)
- galtzo-floss / destination_errors - [![Downloads Rank 🐙:galtzo-floss/destination_errors](https://img.shields.io/gem/rd/destination_errors.svg)](https://bestgems.org/gems/destination_errors)
- galtzo-floss / include_with_respect - [![Downloads Rank 🐙:galtzo-floss/include_with_respect](https://img.shields.io/gem/rd/include_with_respect.svg)](https://bestgems.org/gems/include_with_respect)
- galtzo-floss / seed_migration - [![Downloads Rank 🐙:galtzo-floss/seed_migration](https://img.shields.io/gem/rd/seed_migration.svg)](https://bestgems.org/gems/seed_migration)
- galtzo-floss / shiftable - [![Downloads Rank 🐙:galtzo-floss/shiftable](https://img.shields.io/gem/rd/shiftable.svg)](https://bestgems.org/gems/shiftable)
- galtzo-floss / simple_column-scopes - [![Downloads Rank 🐙:galtzo-floss/simple_column-scopes](https://img.shields.io/gem/rd/simple_column-scopes.svg)](https://bestgems.org/gems/simple_column-scopes)
- galtzo-floss / spyke-connection_lambda - [![Downloads Rank 🐙:galtzo-floss/spyke-connection_lambda](https://img.shields.io/gem/rd/spyke-connection_lambda.svg)](https://bestgems.org/gems/spyke-connection_lambda)
- galtzo-floss / status_tag - [![Downloads Rank 🐙:galtzo-floss/status_tag](https://img.shields.io/gem/rd/status_tag.svg)](https://bestgems.org/gems/status_tag)

</details>

<details>
  <summary>resque & queue plugins</summary>

- galtzo-floss / qfill - [![Downloads Rank 🐙:galtzo-floss/qfill](https://img.shields.io/gem/rd/qfill.svg)](https://bestgems.org/gems/qfill)
- resque / resque-unique_at_runtime - [![Downloads Rank 🐙:resque/resque-unique_at_runtime](https://img.shields.io/gem/rd/resque-unique_at_runtime.svg)](https://bestgems.org/gems/resque-unique_at_runtime)
- resque / resque-unique_by_arity - [![Downloads Rank 🐙:resque/resque-unique_by_arity](https://img.shields.io/gem/rd/resque-unique_by_arity.svg)](https://bestgems.org/gems/resque-unique_by_arity)
- resque / resque-unique_in_queue - [![Downloads Rank 🐙:resque/resque-unique_in_queue](https://img.shields.io/gem/rd/resque-unique_in_queue.svg)](https://bestgems.org/gems/resque-unique_in_queue)

</details>

<details>
  <summary>rspec plugins & testing tools</summary>

- galtzo-floss / activerecord-tablefree - [![Downloads Rank 🐙:galtzo-floss/activerecord-tablefree](https://img.shields.io/gem/rd/activerecord-tablefree.svg)](https://bestgems.org/gems/activerecord-tablefree)
- galtzo-floss / anonymous_active_record - [![Downloads Rank 🐙:galtzo-floss/anonymous_active_record](https://img.shields.io/gem/rd/anonymous_active_record.svg)](https://bestgems.org/gems/anonymous_active_record)
- galtzo-floss / json_schemer-fuzz - [![Downloads Rank 🐙:galtzo-floss/json_schemer-fuzz](https://img.shields.io/gem/rd/json_schemer-fuzz.svg)](https://bestgems.org/gems/json_schemer-fuzz)
- galtzo-floss / rspec-block_is_expected - [![Downloads Rank 🐙:galtzo-floss/rspec-block_is_expected](https://img.shields.io/gem/rd/rspec-block_is_expected.svg)](https://bestgems.org/gems/rspec-block_is_expected)
- galtzo-floss / rspec-pending_for - [![Downloads Rank 🐙:galtzo-floss/rspec-pending_for](https://img.shields.io/gem/rd/rspec-pending_for.svg)](https://bestgems.org/gems/rspec-pending_for)
- galtzo-floss / rspec-stubbed_env - [![Downloads Rank 🐙:galtzo-floss/rspec-stubbed_env](https://img.shields.io/gem/rd/rspec-stubbed_env.svg)](https://bestgems.org/gems/rspec-stubbed_env)
- galtzo-floss / silent_stream - [![Downloads Rank 🐙:galtzo-floss/silent_stream](https://img.shields.io/gem/rd/silent_stream.svg)](https://bestgems.org/gems/silent_stream)
- galtzo-floss / timecop-rspec - [![Downloads Rank 🐙:galtzo-floss/timecop-rspec](https://img.shields.io/gem/rd/timecop-rspec.svg)](https://bestgems.org/gems/timecop-rspec)
- kettle-rb / kettle-soup-cover - [![Downloads Rank 🐙:kettle-rb/kettle-soup-cover](https://img.shields.io/gem/rd/kettle-soup-cover.svg)](https://bestgems.org/gems/kettle-soup-cover)

</details>

<details>
  <summary>rubocop plugins</summary>

Want RuboCop to have its rules explicitly configured for compatibility with the oldest version of Ruby that your library officially supports in two lines of code?

```yaml
inherit_gem:
  rubocop-lts: rubocop-lts.yml # for ruby + rspec
```

More examples for rails-specific, or non-rspec projects are at [rubocop-lts.gitlab.io](https://rubocop-lts.gitlab.io/)

<aside>
  If you think this is what <pre>TargetRubyVersion</pre> does, you've misundertood its purpose, which is to turn off rules that are incompatible with older versions of Ruby, not to make your rules configuration compatible with a specific version of Ruby, nor to turn on Rules that would help with compatibility.
</aside>

- rubocop-lts / rubocop-lts - [![Downloads Rank 🐙:rubocop-lts/rubocop-lts](https://img.shields.io/gem/rd/rubocop-lts.svg)](https://bestgems.org/gems/rubocop-lts)
- rubocop-lts / rubocop-ruby1_8 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby1_8](https://img.shields.io/gem/rd/rubocop-ruby1_8.svg)](https://bestgems.org/gems/rubocop-ruby1_8)
- rubocop-lts / rubocop-ruby1_9 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby1_9](https://img.shields.io/gem/rd/rubocop-ruby1_9.svg)](https://bestgems.org/gems/rubocop-ruby1_9)
- rubocop-lts / rubocop-ruby2_0 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby2_0](https://img.shields.io/gem/rd/rubocop-ruby2_0.svg)](https://bestgems.org/gems/rubocop-ruby2_0)
- rubocop-lts / rubocop-ruby2_1 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby2_1](https://img.shields.io/gem/rd/rubocop-ruby2_1.svg)](https://bestgems.org/gems/rubocop-ruby2_1)
- rubocop-lts / rubocop-ruby2_2 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby2_2](https://img.shields.io/gem/rd/rubocop-ruby2_2.svg)](https://bestgems.org/gems/rubocop-ruby2_2)
- rubocop-lts / rubocop-ruby2_3 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby2_3](https://img.shields.io/gem/rd/rubocop-ruby2_3.svg)](https://bestgems.org/gems/rubocop-ruby2_3)
- rubocop-lts / rubocop-ruby2_4 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby2_4](https://img.shields.io/gem/rd/rubocop-ruby2_4.svg)](https://bestgems.org/gems/rubocop-ruby2_4)
- rubocop-lts / rubocop-ruby2_5 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby2_5](https://img.shields.io/gem/rd/rubocop-ruby2_5.svg)](https://bestgems.org/gems/rubocop-ruby2_5)
- rubocop-lts / rubocop-ruby2_6 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby2_6](https://img.shields.io/gem/rd/rubocop-ruby2_6.svg)](https://bestgems.org/gems/rubocop-ruby2_6)
- rubocop-lts / rubocop-ruby2_7 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby2_7](https://img.shields.io/gem/rd/rubocop-ruby2_7.svg)](https://bestgems.org/gems/rubocop-ruby2_7)
- rubocop-lts / rubocop-ruby3_0 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby3_0](https://img.shields.io/gem/rd/rubocop-ruby3_0.svg)](https://bestgems.org/gems/rubocop-ruby3_0)
- rubocop-lts / rubocop-ruby3_1 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby3_1](https://img.shields.io/gem/rd/rubocop-ruby3_1.svg)](https://bestgems.org/gems/rubocop-ruby3_1)
- rubocop-lts / rubocop-ruby3_2 - [![Downloads Rank 🐙:rubocop-lts/rubocop-ruby3_2](https://img.shields.io/gem/rd/rubocop-ruby3_2.svg)](https://bestgems.org/gems/rubocop-ruby3_2)
- rubocop-lts / standard-rubocop-lts - [![Downloads Rank 🐙:rubocop-lts/standard-rubocop-lts](https://img.shields.io/gem/rd/standard-rubocop-lts.svg)](https://bestgems.org/gems/standard-rubocop-lts)

</details>

I'm attempting to document all of the logos for the FLOSS/FOSS/OSS projects I'm involved in, with their attendant licesnses and copyrights, here:
[logos.galtzo.com](https://logos.galtzo.com).  It has been a multi-year effort hunting down the original creators for some of these logos, and documenting the conditions under which they can be used. I'd love to hear if this is useful in your projects!

I was laid off in a March 2025 RIF, and am looking for my next sponsor and my next role.

[![Liberapay Goal Progress][⛳liberapay-img]][⛳liberapay]
[![Sponsor Me on Github][🖇sponsor-img]][🖇sponsor]
[![Buy me a coffee][🖇buyme-small-img]][🖇buyme]
[![Donate on Polar][🖇polar-img]][🖇polar]
[![Donate to my FLOSS or refugee efforts at ko-fi.com][🖇kofi-img]][🖇kofi]
[![Donate to my FLOSS or refugee efforts using Patreon][🖇patreon-img]][🖇patreon]

---

Want to chat about open source, or any of my projects?  Join my FLOSS discord.

[![Live Chat on Discord][✉️discord-invite-img-ftb]][✉️discord-invite]

Or join the Ruby Friends Squad on Daily.dev

[![Join Me on Daily.dev's RubyFriends][✉️ruby-friends-img]][✉️ruby-friends]

Want to pay me for work? I'm available!

[![Get help from me on Upwork][👨🏼‍🏫expsup-upwork-img]][👨🏼‍🏫expsup-upwork]
[![Get help from me on Codementor][👨🏼‍🏫expsup-codementor-img]][👨🏼‍🏫expsup-codementor]

---

[![Follow Me on Ruby.Social][💖🐘ruby-mast-img]][💖🐘ruby-mast]
[![Follow Me on Bluesky][💖🦋bluesky-img]][💖🦋bluesky]
[![Contact Me][🚂my-contact-img]][🚂my-contact]
[![My technical writing][💖💁🏼‍♂️devto-img]][💖💁🏼‍♂️devto]
[![X (formerly Twitter) Follow][💖❌-img]][💖❌]

---

[![Follow Me on LinkedIn][💖🖇linkedin-img]][💖🖇linkedin]
[![Find Me on WellFound:][💖✌️wellfound-img]][💖✌️wellfound]
[![Find Me on CrunchBase][💖💲crunchbase-img]][💖💲crunchbase]
[![My LinkTree][💖🌳linktree-img]][💖🌳linktree]
[![My Blog][🚂my-blog-img]][🚂my-blog]
[![More About Me][💖💁🏼‍♂️aboutme-img]][💖💁🏼‍♂️aboutme]

[✉️discord-invite]: https://discord.gg/3qme4XHNKN
[✉️discord-invite-img-ftb]: https://img.shields.io/discord/1373797679469170758?style=for-the-badge&logo=discord
[✉️ruby-friends-img]: https://img.shields.io/badge/daily.dev-💎_Ruby_Friends-0A0A0A?style=for-the-badge&logo=dailydotdev&logoColor=white
[✉️ruby-friends]: https://app.daily.dev/squads/rubyfriends

[⛳liberapay-img]: https://img.shields.io/liberapay/goal/pboling.svg?logo=liberapay
[⛳liberapay]: https://liberapay.com/pboling/donate
[🖇sponsor-img]: https://img.shields.io/badge/Sponsor_Me!-pboling.svg?style=social&logo=github
[🖇sponsor]: https://github.com/sponsors/pboling
[🖇polar-img]: https://img.shields.io/badge/polar-donate-yellow.svg
[🖇polar]: https://polar.sh/pboling
[🖇kofi-img]: https://img.shields.io/badge/a_more_different_coffee-✓-yellow.svg
[🖇kofi]: https://ko-fi.com/O5O86SNP4
[🖇patreon-img]: https://img.shields.io/badge/patreon-donate-yellow.svg
[🖇patreon]: https://patreon.com/galtzo
[🖇buyme-img]: https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20latte&emoji=&slug=pboling&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff
[🖇buyme]: https://www.buymeacoffee.com/pboling
[🖇buyme-small-img]: https://img.shields.io/badge/buy_me_a_coffee-✓-yellow.svg?style=flat

[👨🏼‍🏫expsup-upwork]: https://www.upwork.com/freelancers/~014942e9b056abdf86?mp_source=share
[👨🏼‍🏫expsup-upwork-img]: https://img.shields.io/badge/UpWork-13544E?style=for-the-badge&logo=Upwork&logoColor=white
[👨🏼‍🏫expsup-codementor]: https://www.codementor.io/peterboling?utm_source=github&utm_medium=button&utm_term=peterboling&utm_campaign=github
[👨🏼‍🏫expsup-codementor-img]: https://img.shields.io/badge/CodeMentor-Get_Help-1abc9c?style=for-the-badge&logo=CodeMentor&logoColor=white

[🚂my-blog]: http://www.railsbling.com
[🚂my-blog-img]: https://img.shields.io/badge/blog-railsbling-0093D0.svg?style=flat&logo=rubyonrails&logoColor=orange
[🚂my-contact]: http://www.railsbling.com/contact
[🚂my-contact-img]: https://img.shields.io/badge/Contact-Peter_Boling-0093D0.svg?style=flat&logo=rubyonrails&logoColor=red

[💖🖇linkedin]: http://www.linkedin.com/in/peterboling
[💖🖇linkedin-img]: https://img.shields.io/badge/PeterBoling-LinkedIn-0B66C2?style=flat&logo=newjapanprowrestling
[💖✌️wellfound]: https://angel.co/u/peter-boling
[💖✌️wellfound-img]: https://img.shields.io/badge/peter--boling-orange?style=flat&logo=wellfound
[💖💲crunchbase]: https://www.crunchbase.com/person/peter-boling
[💖💲crunchbase-img]: https://img.shields.io/badge/peter--boling-purple?style=flat&logo=crunchbase
[💖🐘ruby-mast]: https://ruby.social/@galtzo
[💖🐘ruby-mast-img]: https://img.shields.io/mastodon/follow/109447111526622197?domain=https%3A%2F%2Fruby.social&style=flat&logo=mastodon&label=Ruby.social%20%40galtzo
[💖🐘social-mast]: https://mastodon.social/@galtzo
[💖🐘social-mast-img]: https://img.shields.io/mastodon/follow/000924127?domain=https%3A%2F%2Fmastodon.social&style=flat&logo=mastodon&label=Mastodon.social%20%40galtzo
[💖🦋bluesky]: https://bsky.app/profile/galtzo.com
[💖🦋bluesky-img]: https://img.shields.io/badge/@galtzo.com-0285FF?style=flat&logo=bluesky&logoColor=white
[💖❌]: https://x.com/@galtzo
[💖❌-img]: https://img.shields.io/twitter/follow/galtzo
[💖🌳linktree]: https://linktr.ee/galtzo
[💖🌳linktree-img]: https://img.shields.io/badge/galtzo-purple?style=flat&logo=linktree
[💖💁🏼‍♂️devto]: https://dev.to/galtzo
[💖💁🏼‍♂️devto-img]: https://img.shields.io/badge/dev.to-0A0A0A?style=flat&logo=devdotto&logoColor=white
[💖💁🏼‍♂️aboutme]: https://about.me/peter.boling
[💖💁🏼‍♂️aboutme-img]: https://img.shields.io/badge/about.me-0A0A0A?style=flat&logo=aboutme&logoColor=white
[💎rubygems]: https://bestgems.org/profiles/pboling
[💎rubygems-img]: https://img.shields.io/gem/u/pboling.svg
[my🧪lab]: https://gitlab.com/pboling
[my🧊berg]: https://codeberg.org/pboling
[my🛖hut]: https://sr.ht/~galtzo/
[rubocop-lts🧪lab]: http://rubocop-lts.gitlab.io/
[ruby-oauth🧪lab]: https://gitlab.com/ruby-oauth

## Sponsors

Thanks to all my sponsors across any of the donation platforms!  Special thanks to my biggest sponsor [HealthSherpa][health-sherpa]!

[![health-sherpa-logo][health-sherpa-logo]][health-sherpa]

[health-sherpa]: https://healthsherpa.com
[health-sherpa-logo]: /assets/img/logos/health-sherpa.png

## Latest FLOSS Releases [![Subscribe to my Rubygems updates][💎rubygems-img]][💎rubygems]

- List is updated frequently by my pet robot: @autobolt

<!-- PBOLINGS-RUBYGEMS:START -->
* 🗓️ 2026-06-01T05:31:36Z | <a href="https://rubygems.org/gems/gitmoji-regex/versions/2.0.1" rel="noopener" target="_blank">gitmoji-regex &lpar;2.0.1&rpar;</a> | 
🏁 A regular expression matching Gitmoji &lpar;a subset of Unicode Emoji&rpar; symbolsFund overlooked open source projects - bottom of stack, dev/test dependencies: floss-funding.dev    
* 🗓️ 2026-05-30T23:39:03Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/24.1.0" rel="noopener" target="_blank">rubocop-lts &lpar;24.1.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T23:37:51Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/22.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;22.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T23:16:13Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/20.3.0" rel="noopener" target="_blank">rubocop-lts &lpar;20.3.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T23:15:04Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/18.3.0" rel="noopener" target="_blank">rubocop-lts &lpar;18.3.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T23:06:04Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/16.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;16.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T23:04:49Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/14.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;14.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T23:03:34Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/12.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;12.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T23:02:04Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/10.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;10.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T23:00:04Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/8.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;8.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T22:57:33Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/6.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;6.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T22:55:44Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/4.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;4.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T22:54:35Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/2.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;2.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T22:51:04Z | <a href="https://rubygems.org/gems/rubocop-lts/versions/0.2.0" rel="noopener" target="_blank">rubocop-lts &lpar;0.2.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby code    
* 🗓️ 2026-05-30T21:54:52Z | <a href="https://rubygems.org/gems/rubocop-ruby3_2/versions/3.0.0" rel="noopener" target="_blank">rubocop-ruby3_2 &lpar;3.0.0&rpar;</a> | 
Configure RuboCop + a bevy of friends to gradually lint Ruby 3.2 code    <!-- PBOLINGS-RUBYGEMS:END -->

## Latest Blog Posts [![My technical writing][💖💁🏼‍♂️devto-img]][💖💁🏼‍♂️devto]

- List is updated frequently by my pet robot: @autobolt

<!-- BLOG-POST-LIST:START -->
* 🗓️ 2026-05-26T22:22:00Z | <a href="https://dev.to/galtzo/why-flagshihtzu-is-changing-its-default-sql-for-bit-flags-41l9" rel="noopener" target="_blank">Why flag_shih_tzu is changing its default SQL for bit flags</a> | 🏷️ ruby, rails, activerecord, bitfield
* 🗓️ 2026-05-25T04:24:26Z | <a href="https://dev.to/galtzo/yard-yaml-011-safer-utf-8-handling-for-yaml-documentation-43jh" rel="noopener" target="_blank">yard-yaml 0.1.1: safer UTF-8 handling for YAML documentation</a> | 🏷️ ruby, rubygems, yard, yaml
* 🗓️ 2026-05-24T06:29:36Z | <a href="https://dev.to/galtzo/yard-fence-090-cleaner-yard-docs-when-markdown-braces-get-in-the-way-2683" rel="noopener" target="_blank">yard-fence 0.9.0: cleaner YARD docs when Markdown braces get in the way</a> | 🏷️ ruby, rubygems, yard, opensource
* 🗓️ 2026-05-24T00:35:28Z | <a href="https://dev.to/galtzo/yard-timekeeper-stop-yard-timestamp-churn-in-checked-in-docs-369o" rel="noopener" target="_blank">yard-timekeeper: Stop YARD Timestamp Churn in Checked-In Docs</a> | 🏷️ ruby, rubygem, yard, opensource
* 🗓️ 2026-04-01T05:59:42Z | <a href="https://dev.to/galtzo/rel-oauth2-v2018-43pf" rel="noopener" target="_blank">💎REL: oauth2 v2.0.18</a> | 🏷️ ruby, oauth, security, github
* 🗓️ 2026-02-18T06:20:33Z | <a href="https://dev.to/galtzo/ann-appraisal2-v306-support-frozen-appraisal-lockfiles-20ml" rel="noopener" target="_blank">🐠 ANN: appraisal2 v3.0.6 - support frozen appraisal lockfiles</a> | 🏷️ news, ruby, testing, tooling
* 🗓️ 2026-02-06T01:00:32Z | <a href="https://dev.to/galtzo/hostile-takeover-of-rubygems-my-thoughts-5hlo" rel="noopener" target="_blank">Hostile Takeover of RubyGems: My Thoughts</a> | 🏷️ opensource, ruby, rails, governance
* 🗓️ 2026-01-19T03:03:27Z | <a href="https://dev.to/galtzo/setup-ruby-flash-25lb" rel="noopener" target="_blank">⚡️ setup-ruby-flash</a> | 🏷️ ruby, gha, ore, rv
* 🗓️ 2025-11-06T23:39:10Z | <a href="https://dev.to/galtzo/floss-funding-2cfn" rel="noopener" target="_blank">💲FLOSS Funding</a> | 🏷️ career, discuss, opensource
* 🗓️ 2025-10-14T00:49:55Z | <a href="https://dev.to/galtzo/ann-omniauth-identity-v315-hanamirom-support-4ha3" rel="noopener" target="_blank">💎 ANN: omniauth-identity v3.1.5 &lpar;Hanami/ROM Support&rpar;</a> | 🏷️ webdev, ruby, rom, authentication
* 🗓️ 2025-09-18T06:30:38Z | <a href="https://dev.to/galtzo/ann-oauth2-v2017-h1a" rel="noopener" target="_blank">💎 ANN: oauth2 v2.0.17</a> | 🏷️ ruby, oauth, webdev, instagram
* 🗓️ 2025-09-15T11:53:14Z | <a href="https://dev.to/galtzo/ann-kettle-dev-v1020-w-improved-changelog-handling-20hl" rel="noopener" target="_blank">💎 ANN: kettle-dev v1.1.20 w/ improved CHANGELOG handling</a> | 🏷️ devtools, ruby, packaging, automation<!-- BLOG-POST-LIST:END -->

# Contributions

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/pboling/pboling/raw/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/pboling/pboling/raw/output/github-snake.svg" />
  <img alt="github-snake" src="github-snake.svg" />
</picture>

![Comment Reactions](https://github.com/pboling/pboling/raw/main/dist/metrics.plugin.reactions.svg?raw=true)
![Notable Contributions](https://github.com/pboling/pboling/raw/main/dist/metrics.plugin.notable.svg?raw=true)

## :child: How it started

<figure>
  <img align="left" width="25%" src="https://railsbling.com/peter-amazon-black-caiman.jpg" alt="Holding a black caiman, Amazon River, Brazil. 1997">
  <figcaption>A cheeky me holding a baby black caiman, Amazon River, Brazil, June 24, 1997, shortly after completing my first programming course - Pascal. The <a href="https://en.wikipedia.org/wiki/Black_caiman">black caiman</a>, a baby specimen of the family Alligatoridae and order Crocodilia, was unharmed, and released back to the water, where it promptly continued following its mother. Full grown they are among the largest alligators and crocodiles in the world<a src="https://github.com/ElectricRCAircraftGuy/eRCaGuy_hello_world/blob/master/markdown/github_readme_center_and_align_images.md">.</a></figcaption>
</figure>

## :godmode: How it's going

- 🦷 I'm putting more of my focus on FLOSS/FOSS/OSS efforts (of myself and others)! <img src="https://img.shields.io/liberapay/gives/pboling.svg?logo=liberapay"> and <img src="https://img.shields.io/liberapay/receives/pboling.svg?logo=liberapay"> from <img src="https://img.shields.io/liberapay/patrons/pboling.svg?logo=liberapay">
- 👷 I build big things and small things out of tiny bits.
- ✨ Recently created [`rubocop-lts`](https://github.com/rubocop-lts) for library maintainer happiness 👩‍❤️‍👩.
- 🔭 I’m working on finishing the migration away from TravisCI to modern CI tools.
- 🌱 I’m learning Svelte & SvelteKit, with Lucia, Drizzle, Zod, Inlang Paraglide, Skeleton, Tailwind, Typescript, and so many more cool tools.
- 👯 Preparing next release of `seed_migrations` and `oauth` gems!
- 🤔 I’ve moved my suite of Resque plugins to the Resque org!
- 📫 How to [reach me](https://about.me/peter.boling)
- 😄 Pronouns: He/Him
- 🗨️ I speak 3 languages fluently, and for a 4th I'm learning Bahasa Indonesia!
- 👷‍♂️ I help refugees and ex-refugees in Ghana🇬🇭 and Liberia🇱🇷, respectively, through Hope For Tomorrow, a Liberian NGO.  DM me if interested in knowing more.

<details>
  <summary>:hammer_and_wrench: My Dev Tools:</summary>
  <div id="tools">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/amazonwebservices/amazonwebservices-original.svg"
       alt="AWS" title="AWS" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bash/bash-plain.svg"
       alt="bash" title="bash" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/circleci/circleci-plain.svg"
       alt="circleci" title="circleci" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/codecov/codecov-plain.svg"
       alt="codecov" title="codecov" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-plain.svg"
       alt="css3" title="css3" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/debian/debian-plain.svg"
       alt="debian" title="debian" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/digitalocean/digitalocean-original.svg"
       alt="digitalocean" title="digitalocean" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-plain.svg"
       alt="docker" title="docker" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-plain.svg"
       alt="git" title="git" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg"
       alt="github" title="github" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/gitlab/gitlab-plain.svg"
       alt="gitlab" title="gitlab" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/gitter/gitter-plain.svg"
       alt="gitter" title="gitter" width="28" height="28" />
    <img src="https://github.com/devicons/devicon/blob/master/icons/graphql/graphql-plain.svg"
       alt="graphql" title="graphql" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/handlebars/handlebars-original.svg"
       alt="handlebars" title="handlebars" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/heroku/heroku-plain.svg"
       alt="heroku" title="heroku" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/jamstack/jamstack-original.svg"
       alt="jamstack" title="jamstack" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-plain.svg"
       alt="javascript" title="javascript" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/jetbrains/jetbrains-original.svg"
       alt="jetbrains" title="jetbrains" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/jira/jira-plain.svg"
       alt="jira" title="jira" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/kubernetes/kubernetes-plain.svg"
       alt="kubernetes" title="kubernetes" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-plain.svg"
       alt="linux" title="linux" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/markdown/markdown-original.svg"
       alt="markdown" title="markdown" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-plain.svg"
       alt="mysql" title="mysql" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/neo4j/neo4j-plain.svg"
       alt="neo4j" title="neo4j" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nodejs/nodejs-plain.svg"
       alt="nodejs" title="nodejs" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-plain.svg"
       alt="postgresql" title="postgresql" width="28" height="28" />
    <img src="https://github.com/devicons/devicon/blob/master/icons/rails/rails-plain.svg"
       alt="rails" title="rails" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/ruby/ruby-plain.svg"
       alt="ruby" title="ruby" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/rubymine/rubymine-plain.svg"
       alt="rubymine" title="rubymine" width="28" height="28" />
    <img src="https://github.com/devicons/devicon/blob/master/icons/svelte/svelte-plain.svg"
       alt="svelte" title="svelte" width="28" height="28" />
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/wordpress/wordpress-plain.svg"
       alt="wordpress" title="wordpress" width="28" height="28" />
  </div>
</details>

---

## :briefcase: Career

- The list is long, even in summary, see [my LinkedIn](https://www.linkedin.com/in/peterboling/).

### :roll_of_paper: Current Roles

- Open Source Contributor, OWASP | [🌪️ OWASP CycloneDX](https://github.com/CycloneDX/cyclonedx-ruby-gem/pulls?q=is%3Apr+author%3Apboling+)
- Open Source Contributor, ASF | [👀 Apache SkyWalking Eyes](https://github.com/apache/skywalking-eyes/pulls?q=is%3Amerged+is%3Apr+author%3Apboling+)
- FLOSS Blogger | [RailsBling](https://dev.to/galtzo)
- FLOSS Author | [RubyGems](https://bestgems.org/profiles/pboling)
- FLOSS Maintainer | [Tidelift Enterprise OSS](https://tidelift.com/subscription/pkg/rubygems-oauth2?utm_source=rubygems-oauth2&utm_medium=referral&utm_campaign=enterprise)
- Researcher | [WordTree Foundation](http://wordtree.org/)

[![Open Hub profile](https://www.openhub.net/accounts/peterboling/widgets/account_detailed?format=gif&amp;ref=sample)](https://www.openhub.net/accounts/peterboling?ref=sample)

<a href="https://github.com/anuraghazra/github-readme-stats#github-stats-card">
  <img align="center" src="https://github-readme-stats.vercel.app/api?username=pboling&count_private=true&show_icons=true&theme=tokyonight" />
</a>

<a href="https://github.com/anuraghazra/github-readme-stats#top-languages-card">
  <img align="center" src="https://github-readme-stats.vercel.app/api/top-langs/?username=pboling&theme=tokyonight&layout=compact&hide=rich%20text%20format" />
</a>
