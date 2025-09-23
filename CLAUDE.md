# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# AI-Driven Automated Upgrade of Legacy Systems

## Project Overview

**Client:** Jing Sun  
**Target System:** Auckland Library Legacy System  
**Migration Target:** Node.js + MongoDB + Solr

This project modernizes Auckland Library's legacy systems using LLM-based code understanding, automated codemods, comprehensive testing, and data migration. The system employs 6 specialized agents working in a coordinated workflow to ensure seamless modernization.

## Development Commands

```bash
# Development setup (to be added when implemented)
npm install                    # Install dependencies
npm run dev                   # Start development server
npm run build                 # Build for production
npm run test                  # Run tests
npm run lint                  # Run linting
npm run typecheck            # Type checking
```

## Architecture Overview

### Agent Workflow Design

**6-Agent Auckland Library Modernization Pipeline:**

1. **CodeUnderstandingAgent** - Legacy system analysis
   - Repository structure analysis (repo tool)
   - Code indexing and search (code-index tool)
   - Code dependency mapping (codegraph tool)
   - Legacy architecture comprehension

2. **ModernizationPlannerAgent** - Migration strategy and approval
   - Software Bill of Materials generation (sbom tool)
   - Vulnerability scanning and security assessment (vuln-scan tool)
   - Migration plan approval workflow (approval-gate tool)
   - Risk assessment and mitigation planning

3. **CodemodAgent** - Automated code transformation
   - LLM-driven code modernization (codemod tool)
   - Build and test integration (build-test tool)
   - Syntax and pattern transformation
   - Framework migration automation

4. **DataMigrationAgent** - Database and search modernization
   - Database profiling and analysis (db-profiler tool)
   - ETL pipeline management (etl tool)
   - Solr configuration and migration (solr-admin tool)
   - Data integrity validation

5. **ValidationAgent** - Quality assurance and testing
   - Automated build and test execution (build-test tool)
   - System observability and monitoring (observability tool)
   - Performance regression testing
   - Integration validation

6. **DocumentationAgent** - Knowledge capture and documentation
   - Automated documentation generation (docgen tool)
   - Migration process documentation
   - System architecture documentation
   - User guide generation

### Backend Architecture

**Core Components:**

- **Agent Engine**: Multi-agent coordination and communication
- **Code Analysis Engine**: Static analysis, AST parsing, dependency graphs
- **Transformation Engine**: Code refactoring, modernization, migration
- **Validation Engine**: Testing, security scanning, performance analysis
- **Knowledge Base**: Upgrade patterns, best practices, technology mappings
- **API Gateway**: External integrations and user interfaces

## Required MCP Servers

### Agent-Specific Tool Integration:

**For CodeUnderstandingAgent:**
1. **Repository MCP** (Custom: `repo` tool)
   - Git repository analysis and structure mapping
   - Legacy codebase exploration and cataloging

2. **Code Index MCP** (Custom: `code-index` tool)
   - Full-text search across codebase
   - Symbol and reference indexing

3. **Code Graph MCP** (Custom: `codegraph` tool)
   - Dependency graph generation
   - Call graph and data flow analysis

**For ModernizationPlannerAgent:**
4. **SBOM MCP** (Custom: `sbom` tool)
   - Software Bill of Materials generation
   - Dependency and license tracking

5. **Vulnerability Scanner MCP** (Custom: `vuln-scan` tool)
   - Security vulnerability assessment
   - CVE database integration

6. **Approval Gate MCP** (Custom: `approval-gate` tool)
   - Workflow approval management
   - Human-in-the-loop decision points

**For CodemodAgent:**
7. **Codemod MCP** (Custom: `codemod` tool)
   - AST-based code transformation
   - LLM-guided modernization patterns

8. **Build Test MCP** (Custom: `build-test` tool)
   - Automated build and test execution
   - CI/CD pipeline integration

**For DataMigrationAgent:**
9. **DB Profiler MCP** (Custom: `db-profiler` tool)
   - Database schema analysis
   - Performance profiling and optimization

10. **ETL MCP** (Custom: `etl` tool)
    - Extract, Transform, Load operations
    - Data migration pipeline management

11. **Solr Admin MCP** (Custom: `solr-admin` tool)
    - Solr configuration and management
    - Search index migration

**For ValidationAgent:**
12. **Observability MCP** (Custom: `observability` tool)
    - System monitoring and metrics collection
    - Performance regression detection

**For DocumentationAgent:**
13. **Doc Generator MCP** (Custom: `docgen` tool)
    - Automated documentation generation
    - Code-to-documentation transformation

### Foundation MCP Servers:
14. **File System MCP** (`@modelcontextprotocol/server-filesystem`)
15. **Git MCP** (`@modelcontextprotocol/server-git`)
16. **SQLite MCP** (`@modelcontextprotocol/server-sqlite`)
17. **Web Search MCP** (`@modelcontextprotocol/server-web-search`)

## Backend Development Tasks

### Phase 1: Foundation & MCP Server Development (Weeks 1-4)

**Your Core Responsibilities:**

1. **Custom MCP Server Development**
   - **Priority 1:** `repo`, `code-index`, `codegraph` MCPs (for CodeUnderstandingAgent)
   - **Priority 2:** `sbom`, `vuln-scan`, `approval-gate` MCPs (for ModernizationPlannerAgent)
   - **Priority 3:** `codemod`, `build-test` MCPs (for CodemodAgent)

2. **Agent Communication Framework**
   - Message passing protocol between 6 agents
   - Event-driven architecture for Auckland Library workflow
   - Agent lifecycle management and coordination

3. **Database Schema for Auckland Library Migration**
   - Legacy system analysis results storage
   - Migration progress tracking
   - Approval workflow state management
   - Solr index migration metadata

4. **API Gateway for Library System Integration**
   - RESTful API for library staff interfaces
   - WebSocket for real-time migration status
   - Integration with existing library authentication

### Phase 2: Agent Backend Implementation (Weeks 5-8)

1. **CodeUnderstandingAgent Backend**
   - Auckland Library legacy code analysis engine
   - Repository structure mapping algorithms
   - Code dependency visualization for library systems

2. **ModernizationPlannerAgent Backend**
   - Library-specific migration strategy algorithms
   - Security vulnerability assessment for library data
   - Approval workflow engine for library stakeholders

3. **CodemodAgent Backend**
   - LLM-driven code transformation engine
   - Auckland Library specific modernization patterns
   - Build and test automation for Node.js migration

4. **DataMigrationAgent Backend**
   - Library database profiling and migration
   - Solr search index modernization
   - ETL pipeline for library catalog data

### Phase 3: Validation & Documentation Systems (Weeks 9-12)

1. **ValidationAgent Backend**
   - Library system integration testing
   - Performance monitoring for MongoDB + Solr stack
   - Regression testing for library operations

2. **DocumentationAgent Backend**
   - Library-specific documentation generation
   - Migration process documentation for library staff
   - System architecture documentation

3. **End-to-End Integration**
   - 6-agent workflow orchestration
   - Auckland Library deployment pipeline
   - Production monitoring and alerting

## Technology Stack

**Backend (Auckland Library Specific):**
- Node.js/TypeScript for agent runtime and target migration stack
- Python for LLM integration and code analysis
- MongoDB for modernized data storage (migration target)
- Solr for search functionality (migration target)
- PostgreSQL for migration metadata and workflow state
- Redis for agent communication and job queues
- Docker for containerized testing and deployment

**AI/ML:**
- OpenAI/Anthropic APIs for LLM-based code understanding
- Local models for sensitive library data analysis
- Vector databases for code similarity and pattern matching
- Custom fine-tuned models for Auckland Library specific patterns

**Auckland Library Integration:**
- Legacy system connectors for existing database
- Solr migration utilities and index management
- Library catalog data transformation tools
- Staff authentication and approval workflows

**Development Tools:**
- Custom MCP servers (13 specialized tools)
- GitHub Actions for CI/CD
- ESLint/Prettier for code quality
- Jest for testing
- Docker Compose for local development

## Security Considerations

- Sandboxed execution environments
- Code sanitization before analysis
- Secure handling of proprietary code
- Audit trails for all modifications
- Permission-based access control

## Success Metrics

- Upgrade success rate (% of projects successfully modernized)
- Time reduction compared to manual upgrades
- Code quality improvement metrics
- Security vulnerability reduction
- Performance improvement measurements