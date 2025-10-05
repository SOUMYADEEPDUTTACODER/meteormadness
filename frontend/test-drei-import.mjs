// test-drei-import.mjs
try {
  const drei = await import('@react-three/drei');
  console.log('✅ @react-three/drei imported successfully!');
  console.log('Available exports:', Object.keys(drei).slice(0, 10)); // show first few exports
} catch (err) {
  console.error('❌ Failed to import @react-three/drei:');
  console.error(err);
  process.exit(1);
}
