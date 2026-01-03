# CIA-SIE Architecture Diagrams

This directory contains professional-grade architecture diagrams in **PlantUML** format.

## Diagram Files

| File | Description |
|------|-------------|
| `system_architecture.puml` | C4-style system architecture with all layers |
| `entity_relationship.puml` | Database entity relationship diagram |
| `signal_ingestion_flow.puml` | Signal processing sequence diagram |
| `kite_oauth_flow.puml` | Zerodha Kite OAuth integration flow |
| `ai_narrative_flow.puml` | AI narrative generation pipeline |
| `constitutional_rules.puml` | Constitutional rules enforcement activity diagram |
| `contradiction_detection.puml` | Exposure engine detection flowchart |
| `user_journey.puml` | Complete user journey state diagram |
| `api_endpoints.puml` | Full API endpoint reference |

## How to View These Diagrams

### Option 1: PlantUML Online Server (Easiest)

1. Go to [PlantUML Web Server](http://www.plantuml.com/plantuml/uml/)
2. Copy the contents of any `.puml` file
3. Paste into the editor
4. View the rendered diagram

### Option 2: VS Code Extension

1. Install the **PlantUML** extension by jebbs
2. Open any `.puml` file
3. Press `Alt+D` to preview

### Option 3: IntelliJ IDEA

1. Install the PlantUML Integration plugin
2. Open any `.puml` file
3. The diagram renders in the preview pane

### Option 4: Command Line

```bash
# Install PlantUML (macOS)
brew install plantuml

# Generate PNG images
plantuml -tpng *.puml

# Generate SVG images
plantuml -tsvg *.puml
```

### Option 5: GitHub Rendering

GitHub natively renders PlantUML diagrams. Simply view the files on GitHub.

## Mermaid Diagrams

For Mermaid-format diagrams (GitHub-native rendering), see:
- `../CIA-SIE_ARCHITECTURE_FLOWCHARTS.md`

GitHub renders Mermaid diagrams automatically in markdown files.

## Diagram Standards

- **Color Scheme:**
  - `#E3F2FD` - External systems (light blue)
  - `#FFF9C4` - API layer (light yellow)
  - `#F3E5F5` - Service layer (light purple)
  - `#E8F5E9` - Data layer (light green)
  - `#FFCCBC` - Platform adapters (light orange)
  - `#FCE4EC` - Storage (light pink)
  - `#C8E6C9` - Success/Pass (green)
  - `#FFCDD2` - Error/Violation (red)

- **Naming Convention:**
  - `*_flow.puml` - Sequence diagrams
  - `*_structure.puml` - Component diagrams
  - `*_journey.puml` - State diagrams
