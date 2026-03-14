import React from 'react';
import { View, StyleSheet } from 'react-native';
import Svg, { Rect, Line } from 'react-native-svg';

interface BreathingWaveformProps {
  data: number[];
}

export default function BreathingWaveform({ data }: BreathingWaveformProps) {
  const width = 320;
  const height = 200;
  const padding = 20;
  const innerWidth = width - 2 * padding;
  const innerHeight = height - 2 * padding;

  return (
    <View style={styles.container}>
      <Svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        {/* Background grid */}
        <Line
          x1={padding}
          y1={padding + innerHeight / 2}
          x2={width - padding}
          y2={padding + innerHeight / 2}
          stroke="#CCCCCC"
          strokeWidth="1"
          strokeDasharray="5,5"
        />

        {/* Waveform bars */}
        {data.map((value, index) => {
          const x = padding + (index / (data.length - 1)) * innerWidth;
          const barHeight = value * innerHeight;
          const barY = padding + innerHeight / 2 - barHeight / 2;

          return (
            <Rect
              key={index}
              x={x - 3}
              y={barY}
              width="6"
              height={barHeight}
              fill="#1976D2"
              opacity={0.8}
            />
          );
        })}
      </Svg>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'white',
    borderRadius: 12,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
  },
});
