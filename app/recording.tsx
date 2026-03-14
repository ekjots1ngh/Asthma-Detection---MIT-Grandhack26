import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { useRouter } from 'expo-router';
import { Audio } from 'expo-av';
import BreathingWaveform from '@/components/breathing-waveform';

export default function RecordingScreen() {
  const router = useRouter();
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [waveformData, setWaveformData] = useState<number[]>(Array(50).fill(0.3));

  const RECORDING_DURATION = 10;

  const stopRecording = useCallback(async () => {
    try {
      if (recording) {
        await recording.stopAndUnloadAsync();
        setIsRecording(false);
        const uri = recording.getURI();
        router.push({
          pathname: '/results',
          params: { recordingUri: uri },
        });
      }
    } catch (error) {
      console.error('Failed to stop recording:', error);
      alert('Failed to stop recording');
    }
  }, [recording, router]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRecording && recordingTime < RECORDING_DURATION) {
      interval = setInterval(() => {
        setRecordingTime((t) => t + 1);
        // Simulate waveform data with random values
        setWaveformData((prev) => {
          const newData = [...prev];
          newData.shift();
          newData.push(Math.random() * 0.8 + 0.2);
          return newData;
        });
      }, 100);
    } else if (recordingTime >= RECORDING_DURATION && isRecording) {
      void stopRecording();
    }
    return () => clearInterval(interval);
  }, [isRecording, recordingTime, stopRecording]);

  const startRecording = async () => {
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (!permission.granted) {
        alert('Permission to access microphone is required');
        return;
      }

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const newRecording = new Audio.Recording();
      await newRecording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
      await newRecording.startAsync();
      setRecording(newRecording);
      setIsRecording(true);
      setRecordingTime(0);
      setWaveformData(Array(50).fill(0.3));
    } catch (error) {
      console.error('Failed to start recording:', error);
      alert('Failed to start recording');
    }
  };


  const handleCancel = () => {
    if (isRecording && recording) {
      recording.stopAndUnloadAsync();
      setIsRecording(false);
      setRecordingTime(0);
    }
    router.back();
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Recording Breathing</Text>

        <View style={styles.instructionsBox}>
          <Text style={styles.instructions}>
            📍 Place the stethoscope bell gently on your child&apos;s chest
          </Text>
          <Text style={styles.instructions}>
            🔇 Keep the room quiet
          </Text>
          <Text style={styles.instructions}>
            ⏱️ Hold still for 10 seconds
          </Text>
        </View>

        <View style={styles.waveformContainer}>
          <BreathingWaveform data={waveformData} />
        </View>

        <View style={styles.timerBox}>
          <Text style={styles.timer}>{recordingTime}s / {RECORDING_DURATION}s</Text>
        </View>

        <View style={styles.buttonContainer}>
          {!isRecording ? (
            <TouchableOpacity
              style={[styles.button, styles.recordButton]}
              onPress={startRecording}
              activeOpacity={0.8}
            >
              <Text style={styles.buttonText}>Start Recording</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              style={[styles.button, styles.stopButton]}
              onPress={stopRecording}
              activeOpacity={0.8}
            >
              <Text style={styles.buttonText}>Stop Recording</Text>
            </TouchableOpacity>
          )}

          <TouchableOpacity
            style={[styles.button, styles.cancelButton]}
            onPress={handleCancel}
            activeOpacity={0.8}
          >
            <Text style={styles.cancelButtonText}>Cancel</Text>
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
  instructionsBox: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 12,
    marginBottom: 20,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
  },
  instructions: {
    fontSize: 16,
    color: '#333',
    marginBottom: 12,
    lineHeight: 24,
  },
  waveformContainer: {
    flex: 1,
    justifyContent: 'center',
    marginBottom: 20,
  },
  timerBox: {
    backgroundColor: 'white',
    paddingVertical: 20,
    borderRadius: 12,
    marginBottom: 20,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
  },
  timer: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1976D2',
  },
  buttonContainer: {
    gap: 12,
  },
  button: {
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 6,
  },
  recordButton: {
    backgroundColor: '#4CAF50',
  },
  stopButton: {
    backgroundColor: '#FF6B6B',
  },
  cancelButton: {
    backgroundColor: '#BDBDBD',
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  cancelButtonText: {
    color: '#333',
    fontSize: 18,
    fontWeight: 'bold',
  },
});
