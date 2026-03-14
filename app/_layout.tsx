import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import 'react-native-reanimated';

export default function RootLayout() {
  return (
    <>
      <Stack>
        <Stack.Screen
          name="index"
          options={{
            headerShown: false,
            title: 'Check Breathing'
          }}
        />
        <Stack.Screen
          name="recording"
          options={{
            headerShown: false,
            title: 'Recording'
          }}
        />
        <Stack.Screen
          name="results"
          options={{
            headerShown: false,
            title: 'Results'
          }}
        />
      </Stack>
      <StatusBar style="auto" />
    </>
  );
}
