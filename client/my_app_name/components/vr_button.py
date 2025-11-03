import reflex as rx


def vr_button() -> rx.Component:
    """Create a VR button as a regular HTML overlay - works with Virtual Desktop."""
    return rx.button(
        "Enter VR",
        id="vr-button",
        on_click=rx.call_script(
            """
            async function toggleVR() {
                const button = document.getElementById('vr-button');
                const canvas = document.querySelector('canvas');
                
                if (!canvas) {
                    alert('Canvas not found');
                    return;
                }
                
                if (!('xr' in navigator)) {
                    alert('WebXR not supported. If using Virtual Desktop, make sure:\\n1. You are in VR mode in Virtual Desktop\\n2. Using a WebXR compatible browser (Chrome/Edge)\\n3. Your VR headset is connected');
                    return;
                }
                
                try {
                    // Check if WebXR is available
                    const isSupported = await navigator.xr.isSessionSupported('immersive-vr');
                    if (!isSupported) {
                        alert('VR not available. For Virtual Desktop:\\n1. Launch Virtual Desktop on your headset\\n2. Connect to your PC\\n3. Try again');
                        return;
                    }
                    
                    // Request VR session with features that work well with Virtual Desktop
                    const session = await navigator.xr.requestSession('immersive-vr', {
                        requiredFeatures: ['local-floor'],
                        optionalFeatures: ['bounded-floor', 'hand-tracking']
                    });
                    
                    // Get the WebGL renderer from the canvas
                    const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
                    if (!gl) {
                        alert('WebGL context not available');
                        return;
                    }
                    
                    // Set up the XR session
                    const renderer = canvas.__THREE_RENDERER__;
                    if (renderer && renderer.xr) {
                        renderer.xr.enabled = true;
                        await renderer.xr.setSession(session);
                    }
                    
                    session.addEventListener('end', () => {
                        button.textContent = 'Enter VR';
                        button.style.backgroundColor = '#3498db';
                        console.log('VR session ended');
                    });
                    
                    button.textContent = 'Exit VR';
                    button.style.backgroundColor = '#e74c3c';
                    console.log('VR session started - works with Virtual Desktop!');
                } catch (error) {
                    console.error('VR Error:', error);
                    alert('Failed to enter VR mode.\\n\\nError: ' + error.message + '\\n\\nFor Virtual Desktop users:\\n• Make sure Virtual Desktop is running on your headset\\n• Your PC must be connected to the same network\\n• Try restarting Virtual Desktop');
                }
            }
            toggleVR();
            """
        ),
        position="fixed",
        bottom="20px",
        right="20px",
        padding="12px 20px",
        background_color="#3498db",
        color="white",
        border="none",
        border_radius="8px",
        cursor="pointer",
        font_size="14px",
        font_weight="bold",
        box_shadow="0 4px 6px rgba(0,0,0,0.3)",
        z_index="10000",
    )




