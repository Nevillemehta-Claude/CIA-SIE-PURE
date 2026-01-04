/**
 * CONSTITUTIONAL RULE COMPLIANCE TESTS
 * 
 * CRITICAL: These tests verify adherence to CIA-SIE's three constitutional rules:
 * 1. Decision support only (no execution commands)
 * 2. Never resolve contradictions
 * 3. Descriptive language only
 */

import { ClaudeAnalysisFixtures } from '../../fixtures/claude/analysis';

describe('Constitutional Rule Compliance', () => {

  // =========================================================================
  // RULE 1: DECISION SUPPORT ONLY
  // =========================================================================

  describe('Rule 1: Decision Support Only - No Execution Commands', () => {
    
    it('should NOT contain BUY/SELL commands in any analysis', () => {
      const allFixtures = [
        ClaudeAnalysisFixtures.GRADE_A,
        ClaudeAnalysisFixtures.GRADE_B,
        ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY,
        ClaudeAnalysisFixtures.GRADE_D,
        ClaudeAnalysisFixtures.GRADE_F,
        ClaudeAnalysisFixtures.NEUTRAL,
        ClaudeAnalysisFixtures.TIMEFRAME_CONTRADICTION
      ];

      const forbiddenPatterns = [
        /\bBUY\b/i,
        /\bSELL\b/i,
        /\bEXECUTE\b/i,
        /\bPLACE ORDER\b/i,
        /\bENTER POSITION\b/i,
        /\bEXIT POSITION\b/i,
        /\bGO LONG\b/i,
        /\bGO SHORT\b/i,
        /\bOPEN TRADE\b/i,
        /\bCLOSE TRADE\b/i
      ];

      allFixtures.forEach(analysis => {
        forbiddenPatterns.forEach(pattern => {
          expect(analysis.rationale).not.toMatch(pattern);
          analysis.bullishFactors.forEach(f => expect(f).not.toMatch(pattern));
          analysis.bearishFactors.forEach(f => expect(f).not.toMatch(pattern));
          analysis.technicalSummary.match(pattern) && 
            fail(`Found forbidden pattern ${pattern} in technicalSummary`);
        });
      });
    });

    it('should NOT contain imperative language', () => {
      const allFixtures = [
        ClaudeAnalysisFixtures.GRADE_A,
        ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY,
        ClaudeAnalysisFixtures.GRADE_F
      ];

      const imperativePatterns = [
        /\byou should\b/i,
        /\byou must\b/i,
        /\brecommend buying\b/i,
        /\brecommend selling\b/i,
        /\bact now\b/i,
        /\bdo not wait\b/i,
        /\btake action\b/i,
        /\bwe recommend\b/i,
        /\bwe suggest\b/i,
        /\bour recommendation\b/i
      ];

      allFixtures.forEach(analysis => {
        imperativePatterns.forEach(pattern => {
          expect(analysis.rationale).not.toMatch(pattern);
        });
      });
    });

    it('should use only descriptive/analytical language', () => {
      const analysis = ClaudeAnalysisFixtures.GRADE_A;
      
      // Should contain descriptive verbs
      const descriptivePatterns = [
        /exhibits?/i,
        /displays?/i,
        /shows?/i,
        /indicates?/i,
        /suggests?/i,
        /demonstrates?/i
      ];
      
      const hasDescriptive = descriptivePatterns.some(p => p.test(analysis.rationale));
      expect(hasDescriptive).toBe(true);
    });

    it('should NOT contain price targets', () => {
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      const priceTargetPatterns = [
        /target price/i,
        /price target/i,
        /expected to reach/i,
        /should reach/i,
        /will hit/i,
        /upside target/i,
        /downside target/i
      ];

      allFixtures.forEach(analysis => {
        priceTargetPatterns.forEach(pattern => {
          expect(analysis.rationale).not.toMatch(pattern);
        });
      });
    });
  });

  // =========================================================================
  // RULE 2: NEVER RESOLVE CONTRADICTIONS
  // =========================================================================

  describe('Rule 2: Never Resolve Contradictions', () => {
    
    it('should PRESERVE contradictions when present', () => {
      const analysis = ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY;
      
      expect(analysis.contradictions).toBeDefined();
      expect(analysis.contradictions.length).toBeGreaterThan(0);
    });

    it('should have at least 3 contradictions in contradictory analysis', () => {
      const analysis = ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY;
      expect(analysis.contradictions.length).toBeGreaterThanOrEqual(3);
    });

    it('should NOT contain resolution language', () => {
      const contradictoryFixtures = [
        ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY,
        ClaudeAnalysisFixtures.TIMEFRAME_CONTRADICTION
      ];

      const resolutionPatterns = [
        /\bon balance\b/i,
        /\boverall\s+(?:the\s+)?(?:signals?\s+)?(?:is|are|suggests?)\s+(?:bullish|bearish)\b/i,
        /\bnet\s+(?:bullish|bearish)\b/i,
        /\btherefore\s+(?:bullish|bearish)\b/i,
        /\bthe\s+(?:bullish|bearish)\s+factors?\s+outweigh\b/i,
        /\bin conclusion\s+(?:bullish|bearish)\b/i,
        /\bdespite.*we believe\b/i,
        /\bweighing the evidence\b/i
      ];

      contradictoryFixtures.forEach(analysis => {
        resolutionPatterns.forEach(pattern => {
          expect(analysis.rationale).not.toMatch(pattern);
        });
      });
    });

    it('should present BOTH sides when contradictions exist', () => {
      const analysis = ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY;
      
      if (analysis.contradictions.length > 0) {
        expect(analysis.bullishFactors.length).toBeGreaterThan(0);
        expect(analysis.bearishFactors.length).toBeGreaterThan(0);
      }
    });

    it('should have LOWER confidence when contradictions present', () => {
      const clearAnalysis = ClaudeAnalysisFixtures.GRADE_A;
      const contradictoryAnalysis = ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY;
      
      expect(contradictoryAnalysis.confidence).toBeLessThan(clearAnalysis.confidence);
    });

    it('should have Grade C for contradictory analysis', () => {
      const analysis = ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY;
      expect(analysis.grade).toBe('C');
    });

    it('should acknowledge contradictions explicitly in rationale', () => {
      const analysis = ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY;
      
      // Should mention contradiction-related terms
      const acknowledgmentPatterns = [
        /contradict/i,
        /conflict/i,
        /opposing/i,
        /mixed/i,
        /divergent/i
      ];
      
      const hasAcknowledgment = acknowledgmentPatterns.some(p => p.test(analysis.rationale));
      expect(hasAcknowledgment).toBe(true);
    });

    it('should include disclaimer about interpretation in contradictory analysis', () => {
      const analysis = ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY;
      
      // Should contain interpretive disclaimer
      const disclaimerPatterns = [
        /market participants may interpret/i,
        /presented as observed/i,
        /without resolution/i,
        /different.*may.*interpret differently/i
      ];
      
      const hasDisclaimer = disclaimerPatterns.some(p => p.test(analysis.rationale));
      expect(hasDisclaimer).toBe(true);
    });
  });

  // =========================================================================
  // RULE 3: DESCRIPTIVE LANGUAGE ONLY
  // =========================================================================

  describe('Rule 3: Descriptive Language Only', () => {
    
    it('should use descriptive verbs, not imperatives', () => {
      const allFixtures = [
        ClaudeAnalysisFixtures.GRADE_A,
        ClaudeAnalysisFixtures.GRADE_B,
        ClaudeAnalysisFixtures.GRADE_C_CONTRADICTORY,
        ClaudeAnalysisFixtures.GRADE_D,
        ClaudeAnalysisFixtures.GRADE_F,
        ClaudeAnalysisFixtures.NEUTRAL
      ];

      const descriptivePatterns = [
        /exhibits?/i,
        /displays?/i,
        /shows?/i,
        /indicates?/i,
        /suggests?/i,
        /demonstrates?/i,
        /presents?/i,
        /reflects?/i
      ];

      allFixtures.forEach(analysis => {
        const hasDescriptive = descriptivePatterns.some(p => p.test(analysis.rationale));
        expect(hasDescriptive).toBe(true);
      });
    });

    it('should frame factors as observations, not recommendations', () => {
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      allFixtures.forEach(analysis => {
        analysis.bullishFactors.forEach(factor => {
          // Should NOT reference "you" or "your" or "we"
          expect(factor).not.toMatch(/\byou\b|\byour\b|\bwe\b|\bour\b/i);
        });
        
        analysis.bearishFactors.forEach(factor => {
          expect(factor).not.toMatch(/\byou\b|\byour\b|\bwe\b|\bour\b/i);
        });
      });
    });

    it('should use past or present tense, not future predictions', () => {
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      const futurePatterns = [
        /\bwill definitely\b/i,
        /\bwill certainly\b/i,
        /\bguaranteed to\b/i,
        /\bis certain to\b/i,
        /\bwill surely\b/i
      ];

      allFixtures.forEach(analysis => {
        futurePatterns.forEach(pattern => {
          expect(analysis.rationale).not.toMatch(pattern);
        });
      });
    });

    it('should NOT use emotional or sensational language', () => {
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      const emotionalPatterns = [
        /\bamazing\b/i,
        /\bincredible\b/i,
        /\bunbelievable\b/i,
        /\bfantastic\b/i,
        /\bterrible\b/i,
        /\bdisaster\b/i,
        /\bcrash\b/i,
        /\bexplosive\b/i,
        /\bmoon\b/i,
        /\brocket\b/i
      ];

      allFixtures.forEach(analysis => {
        emotionalPatterns.forEach(pattern => {
          expect(analysis.rationale).not.toMatch(pattern);
        });
      });
    });

    it('should maintain neutral tone throughout', () => {
      const analysis = ClaudeAnalysisFixtures.GRADE_A;
      
      // Even bullish analysis should be neutral in tone
      expect(analysis.rationale).not.toMatch(/\bget rich\b/i);
      expect(analysis.rationale).not.toMatch(/\bmissing out\b/i);
      expect(analysis.rationale).not.toMatch(/\bonce in a lifetime\b/i);
    });
  });

  // =========================================================================
  // ADDITIONAL COMPLIANCE CHECKS
  // =========================================================================

  describe('Additional Compliance Checks', () => {
    
    it('should have valid grade for all fixtures', () => {
      const validGrades = ['A', 'B', 'C', 'D', 'F'];
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      allFixtures.forEach(analysis => {
        expect(validGrades).toContain(analysis.grade);
      });
    });

    it('should have confidence between 0 and 100', () => {
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      allFixtures.forEach(analysis => {
        expect(analysis.confidence).toBeGreaterThanOrEqual(0);
        expect(analysis.confidence).toBeLessThanOrEqual(100);
      });
    });

    it('should have timestamp in valid ISO format', () => {
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      allFixtures.forEach(analysis => {
        expect(() => new Date(analysis.timestamp)).not.toThrow();
        expect(new Date(analysis.timestamp).toISOString()).toBe(analysis.timestamp);
      });
    });

    it('should have both technical summary and risk assessment', () => {
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      allFixtures.forEach(analysis => {
        expect(analysis.technicalSummary).toBeDefined();
        expect(analysis.technicalSummary.length).toBeGreaterThan(0);
        expect(analysis.riskAssessment).toBeDefined();
        expect(analysis.riskAssessment.length).toBeGreaterThan(0);
      });
    });

    it('should have at least one bullish OR bearish factor', () => {
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      allFixtures.forEach(analysis => {
        const totalFactors = analysis.bullishFactors.length + analysis.bearishFactors.length;
        expect(totalFactors).toBeGreaterThan(0);
      });
    });

    it('should have risk assessment mention support levels', () => {
      const allFixtures = Object.values(ClaudeAnalysisFixtures);
      
      allFixtures.forEach(analysis => {
        const hasLevelInfo = /support|resistance|level/i.test(analysis.riskAssessment);
        expect(hasLevelInfo).toBe(true);
      });
    });
  });
});

