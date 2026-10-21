'use strict';
/* Small red-only bloom pass. Neutral metal and white packet cores stay crisp. */
window.BCNeonBloom = class {
  constructor(renderer) {
    const T=THREE;
    this.renderer=renderer;
    const type=renderer.extensions.has('EXT_color_buffer_float')?T.HalfFloatType:T.UnsignedByteType;
    this.sceneTarget=new T.WebGLRenderTarget(1,1,{type,depthBuffer:true});
    this.glowTarget=new T.WebGLRenderTarget(1,1,{type,depthBuffer:false});
    const vertexShader='varying vec2 vUv; void main(){vUv=uv;gl_Position=vec4(position.xy,0.0,1.0);}';
    this.horizontal=new T.ShaderMaterial({depthTest:false,depthWrite:false,toneMapped:false,
      uniforms:{source:{value:this.sceneTarget.texture},stepSize:{value:new T.Vector2(1,0)}},vertexShader,
      fragmentShader:`uniform sampler2D source; uniform vec2 stepSize; varying vec2 vUv;
        vec3 redLight(vec2 uv){vec3 c=texture2D(source,clamp(uv,0.0,1.0)).rgb;
          float e=clamp(c.r-max(c.g,c.b)*1.35-0.35,0.0,2.5);return vec3(e,e*.002,e*.014);}
        void main(){vec3 c=redLight(vUv)*.227027;
          c+=(redLight(vUv+stepSize)+redLight(vUv-stepSize))*.194595;
          c+=(redLight(vUv+stepSize*2.)+redLight(vUv-stepSize*2.))*.121622;
          c+=(redLight(vUv+stepSize*3.)+redLight(vUv-stepSize*3.))*.054054;
          c+=(redLight(vUv+stepSize*4.)+redLight(vUv-stepSize*4.))*.016216;
          gl_FragColor=vec4(c,1.);}`});
    this.composite=new T.ShaderMaterial({depthTest:false,depthWrite:false,toneMapped:true,
      uniforms:{source:{value:this.sceneTarget.texture},glow:{value:this.glowTarget.texture},stepSize:{value:new T.Vector2(0,1)}},vertexShader,
      fragmentShader:`uniform sampler2D source; uniform sampler2D glow; uniform vec2 stepSize; varying vec2 vUv;
        vec3 sampleGlow(vec2 uv){return texture2D(glow,clamp(uv,0.0,1.0)).rgb;}
        void main(){vec3 c=sampleGlow(vUv)*.227027;
          c+=(sampleGlow(vUv+stepSize)+sampleGlow(vUv-stepSize))*.194595;
          c+=(sampleGlow(vUv+stepSize*2.)+sampleGlow(vUv-stepSize*2.))*.121622;
          c+=(sampleGlow(vUv+stepSize*3.)+sampleGlow(vUv-stepSize*3.))*.054054;
          c+=(sampleGlow(vUv+stepSize*4.)+sampleGlow(vUv-stepSize*4.))*.016216;
          gl_FragColor=vec4(texture2D(source,vUv).rgb+c*.32,1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`});
    this.screen=new T.Scene();this.camera=new T.OrthographicCamera(-1,1,1,-1,0,1);
    this.quad=new T.Mesh(new T.PlaneGeometry(2,2),this.horizontal);this.quad.frustumCulled=false;this.screen.add(this.quad);
  }
  setSize(width,height){
    const w=Math.max(1,Math.round(width)),h=Math.max(1,Math.round(height));
    this.sceneTarget.setSize(w,h);this.glowTarget.setSize(Math.ceil(w/2),Math.ceil(h/2));
    this.horizontal.uniforms.stepSize.value.set(2/w,0);
    this.composite.uniforms.stepSize.value.set(0,2/Math.ceil(h/2));
  }
  render(scene,camera){
    const r=this.renderer,previous=r.getRenderTarget();
    r.setRenderTarget(this.sceneTarget);r.render(scene,camera);
    this.quad.material=this.horizontal;r.setRenderTarget(this.glowTarget);r.render(this.screen,this.camera);
    this.quad.material=this.composite;r.setRenderTarget(previous);r.render(this.screen,this.camera);
  }
};
