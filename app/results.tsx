import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';

type RiskLevel = 'clear' | 'warning' | 'concerning';

interface RiskInfo {
  level: RiskLevel;
  title: string;
  color: string;
  emoji: string;
  message: string;
  recommendation: string;
}

const RISK_INFO: Record<RiskLevel, RiskInfo> = {
  clear: {
    level: 'clear',
    title: 'Clear Breathing',
    color: '#4CAF50',
    emoji: '✓',
    message: 'Your child\'s breathing sounds normal.',
    recommendation: 'Continue regular check-ups.',
  },
  warning: {
    level: 'warning',
    title: 'Possible Wheezing',
    color: '#FFC107',
    emoji: '⚠',
    message: 'We detected some irregular breathing patterns.',
    recommendation: 'Consider consulting with a healthcare provider.',
  },
  concerning: {
    level: 'concerning',
    title: 'Concerning Wheezing',
    color: '#F44336',
    emoji: '⚠',
    message: 'We detected significant breathing concerns.',
    recommendation: 'Please contact your healthcare provider soon.',
  },
};

export default function ResultsScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const [riskLevel, setRiskLevel] = useState<RiskLevel>('clear');

  useEffect(() => {
    // Simulate breathing analysis
    // In a real app, this would analyze the audio file
    const randomLevel = Math.random();
    if (randomLevel < 0.5) {
      setRiskLevel('clear');
    } else if (randomLevel < 0.8) {
      setRiskLevel('warning');
    } else {
      setRiskLevel('concerning');
    }
  }, [params.recordingUri]);

  const risk = RISK_INFO[riskLevel];

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Results</Text>

        <View style={[styles.resultCard, { backgroundColor: risk.color }]}>
          <Text style={styles.emoji}>{risk.emoji}</Text>
          <Text style={styles.resultTitle}>{risk.title}</Text>
          <Text style={styles.resultMessage}>{risk.message}</Text>
        </View>

        <View style={styles.recommendationBox}>
          <Text style={styles.recommendationLabel}>Next Steps:</Text>
          <Text style={styles.recommendationText}>{risk.recommendation}</Text>
        </View>

        <View style={styles.infoBox}>
          <Text style={styles.infoTitle}>About This Assessment</Text>
          <Text style={styles.infoText}>
            This screening tool provides preliminary guidance based on breathing sounds. It is not a medical diagnosis. Always consult with a healthcare professional for medical advice.
          </Text>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={() => router.push('/index')}
            activeOpacity={0.8}
          >
            <Text style={styles.buttonText}>Check Another Child</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => router.back()}
            activeOpacity={0.8}
          >
            <Text style={styles.secondaryButtonText}>Re-record</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#E8F5FF',
  },
  content: {
    flex: 1,
    padding: 20,
    justifyContent: 'space-between',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#1976D2',
    marginBottom: 20,
    textAlign: 'center',
  },
  resultCard: {
    borderRadius: 16,
    paddingVertical: 30,
    paddingHorizontal: 20,
    alignItems: 'center',
    marginBottom: 20,
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
  },
  emoji: {
    fontSize: 64,
    marginBottom: 12,
  },
  resultTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 12,
    textAlign: 'center',
  },
  resultMessage: {
    fontSize: 16,
    color: 'white',
    textAlign: 'center',
    lineHeight: 24,
  },
  recommendationBox: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginBottom: 16,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
  },
  recommendationLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1976D2',
    marginBottom: 8,
  },
  recommendationText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 22,
  },
  infoBox: {
    backgroundColor: '#FFF9C4',
    padding: 16,
    borderRadius: 12,
    marginBottom: 20,
    borderLeftWidth: 4,
    borderLeftColor: '#F57F17',
  },
  infoTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#F57F17',
    marginBottom: 8,
  },
  infoText: {
    fontSize: 13,
    color: '#666',
    lineHeight: 20,
  },
  buttonContainer: {
    gap: 12,
  },
  primaryButton: {
    backgroundColor: '#1976D2',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 6,
  },
  secondaryButton: {
    backgroundColor: 'white',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: '#1976D2',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  secondaryButtonText: {
    color: '#1976D2',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
