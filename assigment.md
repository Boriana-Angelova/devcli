DevCLI a Python command-line tool for static code analysis. It scans Python files and directories, applies rule-based analysis using the AST module, and generates structured Markdown reports. The project was developed with the assistance of AI-powered development tools, which supported different stages of the implementation process, including architecture design, code generation, and iterative refinement of analysis features. AI tools were used to accelerate development, generate initial code structures, and explore alternative approaches for parsing, rule evaluation, and CLI interaction. This AI-assisted workflow allowed for faster prototyping and helped improve the modular design of the system while maintaining flexibility for future extensions.
The project is suitable for Python developers, QA engineers, and DevOps teams who want to automate static code analysis, improve code quality, and integrate automated checks into development workflows and CI/CD pipelines.
Functional Requirements

- CLI must accept multiple file paths and directories. 
- Recursive file analysis with Python AST parsing. 
- Generate structured Markdown reports with errors/warnings. 
- Allow adding custom rules for static analysis. 


Non-Functional Requirements

- Performance: Analysis should scale for large codebases efficiently. 
- Extensibility: Easy to add new rules and analysis modules. 
- Usability: Clear CLI interface with descriptive help messages. 
- Maintainability: Modular code and standardized data structures. 
- Compatibility: Works on Python 3.9+ across platforms (Windows, Linux, macOS).
System Architecture
The system is organized into clearly separated technological modules to ensure modularity, maintainability, and scalability. Each module has a well-defined responsibility and interacts with other components through structured interfaces. Artificial intelligence tools were used during development to accelerate implementation, improve code quality, and assist with architectural decisions.
The main modules of the system include the Command-Line Interface (CLI) layer, the execution and orchestration layer, the static analysis engine, the traceback parsing module, the reporting layer, and the data models layer. The CLI layer handles user interaction and command parsing. The execution layer manages workflow coordination and file processing. The analysis engine performs AST-based static code analysis using rule-based logic. The traceback parser extracts structured information from error messages. The reporting layer generates formatted Markdown output. The data models layer defines standardized structures for representing results and ensuring consistency across the system.
For each module, the development approach followed the same structured process. First, the responsibilities of the module were clearly defined. Second, the internal logic and dependencies were designed. Third, AI tools were used to generate scaffolding code, improve structure, and suggest optimizations. Finally, each module was tested independently to ensure correctness before integration.
Artificial intelligence assisted in multiple ways, including generating boilerplate code, designing AST traversal logic, improving error handling, refining architecture decisions, and creating reusable templates. AI tools were also used to validate design choices, improve documentation quality, and enhance code readability. This AI-assisted workflow significantly accelerated development while maintaining clean architecture principles.
The modular design ensures that new features, such as additional analysis rules, alternative output formats, or integration with external systems, can be added without modifying the core structure of the application.
Development Process per Module:
1) CLI Layer (cli.py)
Description :
Handles the command-line interface, argument parsing, and task execution.
Approach & AI assistance:
•	Defined commands (analyze, runfiles).
•	AI assisted in generating Typer CLI boilerplate and argument handling.
Development Process :
•	Planning: Determine commands and parameters.
•	Workflow: Scaffold CLI using AI prompts.
•	Testing: Run sample commands (devcli --help, devcli analyze).
•	Tool Choice: GitHub Copilot.
________________________________________
2) Execution Layer (runner.py)
Description :
Orchestrates file handling, recursive Python file discovery, and analysis execution.
Development Process:
•	Planning: Define function to start analysis.
•	Workflow: “Generate Python function to recursively find Python files from a path list.”
•	Testing: Unit tests on sample Python files.
•	Tool Choice: GitHub Copilot.
________________________________________
3) Static Analysis Engine (parser.py)
Description:
Performs AST-based static analysis on Python files, extracting functions, classes, imports, and TODO comments.
Development Process / Процес на разработка:
•	Planning: Decide metrics to extract per file.
•	Workflow: “Generate a Python function to parse a file and extract AST info.”
•	Testing: Unit tests on sample .py files.
•	Tool Choice: GitHub Copilot.
________________________________________
4) Rule-Based Failure Analyzer (failure_analyzer.py / analyzer.py)
Description :
Analyzes FailureInfo objects using heuristic rules to detect root causes and suggest fixes.
Development Process:
•	Planning: Define rules for exception types.
•	Workflow: “Generate Python class to analyze failure info and suggest fixes.”
•	Testing: Validated with real tracebacks.
•	Tool Choice: GitHub Copilot.
________________________________________
5) Reporting Layer (reporter.py)
Description:
Generates Markdown reports (analysis_report.md or failure_report.md) with structured summaries.
Development Process :
•	Planning: Define report structure and metrics.
•	Workflow: “Generate function to produce Markdown with headers and tables.”
•	Testing: Visual inspection and CI validation.
•	Tool Choice: GitHub Copilot.
________________________________________
6) AST Utilities (ast_utils.py)
Description:
Helper functions to traverse Python AST and extract functions, classes, imports, and TODOs.
Development Process:
•	Planning: Create reusable utilities for AST analysis.
•	Workflow: “Write AST walker functions to collect functions, classes, and comments.”
•	Testing: Verified extraction from multiple Python files.
•	Tool Choice: GitHub Copilot.
________________________________________
7) Models & Data Structures (models.py)
Description:
Defines data classes for FileAnalysis, FailureInfo, and structured analysis results.
Development Process:
•	Planning: Identify required fields: file_path, functions, classes, todos, error info.
•	Workflow: “Write data classes with fields: file_path, error_message, line_num, function_name.”
•	Testing: Verified serialization, deserialization, and integration.
•	Tool Choice: GitHub Copilot.
________________________________________
8) Traceback Parser (traceback_parser.py)
Description:
Parses Python traceback strings into structured FailureInfo objects.
Development Process:
•	Planning: Identify parsing patterns for tracebacks.
•	Workflow: “Generate parser for Python exception tracebacks into structured objects.”
•	Testing: Validated with real traceback examples.
•	Tool Choice: GitHub Copilot.

Challenges & Tool Comparison

Biggest Challenges:

•	Designing an extensible rule engine - The architecture had to support adding new rules without modifying the core analyzer logic. This required careful modularization so that each rule could be implemented as an independent component that processes parsed AST nodes and returns structured results. The final design ensures that additional rules—such as complexity checks, dependency analysis, or style validation—can be integrated with minimal changes to the existing system.

•	Ensuring reliable CLI input/output tests - Testing CLI applications presents unique challenges because input and output occur through the command line rather than traditional function calls. The main difficulty was validating that the CLI correctly processes different user inputs while producing consistent and readable output.

Tool Comparison:

GitHub Copilot was the most helpful tool for generating boilerplate code, scaffolding modules, and creating repetitive structures. It accelerated the development of the CLI layer, data models, and reporting templates by suggesting complete code snippets based on the context. 

Claude Code was particularly useful for complex logical reasoning tasks that required understanding and manipulating program structure. It excelled in generating AST traversal logic and rule-based analysis engines. 

Cursor and Augment were mainly used for code navigation, refactoring, and improving maintainability. Cursor helped quickly locate and edit related code across multiple files, while Augment assisted in restructuring code to be more modular and readable. They were particularly useful when adding new analysis rules or updating the reporting layer without introducing bugs or inconsistencies.

Overall, the combination of these tools allowed a highly efficient development workflow. Copilot handled scaffolding and repetitive tasks, Claude Code supported reasoning-heavy modules like the AST analysis engine, and Cursor/Augment ensured maintainability and seamless navigation across the codebase. Using them together created a balanced approach, where AI accelerated both coding and architectural refinement.

Future Improvements:

•	Create custom prompts for specific analysis rules - A future improvement would be the introduction of configurable AI prompts tailored for specific code analysis tasks. Instead of relying solely on static AST-based rules, the tool could allow developers to define custom prompts that guide an AI model in evaluating particular aspects of the codebase.

•	Integrate AI-powered lint suggestions in real time - Another improvement would be integrating AI-powered linting suggestions directly into the analysis workflow. Instead of only reporting structural metrics, the tool could analyze the code and generate contextual improvement suggestions.

•	Expand testing for corner cases and edge inputs - While the current testing strategy validates the core functionality of the CLI tool, additional tests could improve robustness and reliability. Future work would focus on expanding the test suite to cover a wider range of corner cases and edge inputs.



 
