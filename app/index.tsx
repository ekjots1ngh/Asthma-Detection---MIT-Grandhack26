import { View, Text, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { useRouter } from 'expo-router';

export default function HomeScreen() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Breathing Check</Text>
        <Text style={styles.subtitle}>Monitor your child&apos;s breathing</Text>

        <TouchableOpacity
          style={styles.largeButton}
          onPress={() => router.push('/recording')}
          activeOpacity={0.8}
        >
          <Text style={styles.buttonText}>Check My Child&apos;s Breathing</Text>
        </TouchableOpacity>

        <Text style={styles.hint}>Place your stethoscope and record a 10-second sample</Text>
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
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#1976D2',
    marginBottom: 10,
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 18,
    color: '#555',
    marginBottom: 40,
    textAlign: 'center',
  },
  largeButton: {
    backgroundColor: '#1976D2',
    paddingVertical: 30,
    paddingHorizontal: 40,
    borderRadius: 20,
    marginBottom: 30,
    width: '90%',
    alignItems: 'center',
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  hint: {
    fontSize: 14,
    color: '#777',
    textAlign: 'center',
    marginTop: 20,
  },
});
