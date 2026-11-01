import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { CSS2DRenderer, CSS2DObject } from "three/examples/jsm/renderers/CSS2DRenderer.js";

export type GNode = { id: string; label: string; kind: string };
export type GEdge = { a: string; b: string; rel: string; src: string };

export const REL: Record<string, { color: string; label: string; dash?: boolean }> = {
  accountable: { color: "#3B4A2F", label: "Accountable" },
  funds: { color: "#8aa548", label: "Funds" },
  houses: { color: "#6b8f9c", label: "Houses" },
  steers: { color: "#b08a3a", label: "Steers" },
  oversees: { color: "#9a7fb0", label: "Oversees" },
  delivers: { color: "#4f8a6b", label: "Delivers work" },
  partners: { color: "#a3ab98", label: "Partners" },
  empowers: { color: "#2f6f8f", label: "Legal basis" },
  access: { color: "#c0703a", label: "Model access" },
  missing: { color: "#b5532f", label: "No stated link", dash: true },
};
// vertical tier by relation: up = power and money, down = delivery and partners
const TIER: Record<string, number> = { accountable: 1.25, funds: 1.0, empowers: 1.35, steers: 0.6, oversees: 0.8, houses: -0.15, access: -0.2, delivers: -1.0, partners: -1.15, missing: -0.6 };

export class NetScene {
  el: HTMLElement; renderer: THREE.WebGLRenderer; labels: CSS2DRenderer; scene = new THREE.Scene();
  camera: THREE.PerspectiveCamera; controls: OrbitControls; group = new THREE.Group(); dashed: THREE.LineDashedMaterial[] = [];
  raf = 0; reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  constructor(el: HTMLElement) {
    this.el = el;
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setPixelRatio(Math.min(2, window.devicePixelRatio));
    el.appendChild(this.renderer.domElement);
    this.labels = new CSS2DRenderer(); this.labels.domElement.style.position = "absolute"; this.labels.domElement.style.top = "0"; this.labels.domElement.style.pointerEvents = "none";
    el.appendChild(this.labels.domElement);
    this.camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100); this.camera.position.set(0, 2.2, 13.5);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true; this.controls.minDistance = 7; this.controls.maxDistance = 34; this.controls.enablePan = false;
    this.controls.autoRotate = !this.reduce; this.controls.autoRotateSpeed = 0.6;
    this.scene.add(new THREE.AmbientLight(0xffffff, 0.9));
    const d = new THREE.DirectionalLight(0xffffff, 0.8); d.position.set(3, 5, 6); this.scene.add(d);
    this.scene.add(this.group);
    new ResizeObserver(() => this.resize()).observe(el); this.resize();
    const loop = () => { this.raf = requestAnimationFrame(loop); this.controls.update(); for (const m of this.dashed) (m as any).dashOffset = ((m as any).dashOffset ?? 0) - 0.01; this.renderer.render(this.scene, this.camera); this.labels.render(this.scene, this.camera); };
    loop();
  }
  resize() { const w = this.el.clientWidth, h = Math.max(520, this.el.clientHeight); this.renderer.setSize(w, h); this.labels.setSize(w, h); this.camera.aspect = w / h; const dist = Math.max(13.5, 5.4 / (Math.tan((34 / 2) * Math.PI / 180) * (w / h))); this.camera.position.setLength(dist); this.camera.updateProjectionMatrix(); }
  dispose() { cancelAnimationFrame(this.raf); this.renderer.dispose(); this.el.innerHTML = ""; }
  clear() { for (const c of [...this.group.children]) { this.group.remove(c); c.traverse((o: any) => { if (o.element) o.element.remove(); o.geometry?.dispose?.(); }); } this.dashed = []; }
  show(nodes: GNode[], edges: GEdge[], instLabel: string) {
    this.clear();
    const pos = new Map<string, THREE.Vector3>(); pos.set("i", new THREE.Vector3(0, 0, 0));
    // group outer nodes by their main relation to the institute, spread them around a ring per tier
    const rel = new Map<string, string>();
    for (const e of edges) { const other = e.b === "i" ? e.a : e.a === "i" ? e.b : null; if (other && !rel.has(other)) rel.set(other, e.rel); }
    for (const e of edges) { if (!rel.has(e.a)) rel.set(e.a, e.rel); }
    const outer = nodes.filter(n => n.id !== "i");
    outer.forEach((n, k) => {
      const ang = (k / outer.length) * Math.PI * 2 + 0.4; const r = 3.8;
      const y = (TIER[rel.get(n.id) ?? "partners"] ?? 0) * 1.9 + (k % 2 ? 0.35 : -0.35);
      pos.set(n.id, new THREE.Vector3(Math.cos(ang) * r, y, Math.sin(ang) * r));
    });
    const css = getComputedStyle(document.documentElement);
    const col = (v: string) => new THREE.Color(css.getPropertyValue(v).trim() || "#6B7F3A");
    for (const n of nodes) {
      const p = pos.get(n.id)!; const isI = n.id === "i";
      const geo = isI ? new THREE.IcosahedronGeometry(0.55, 2) : new THREE.SphereGeometry(0.22, 24, 16);
      const mat = new THREE.MeshStandardMaterial({ color: isI ? col("--g") : n.kind === "ind" ? new THREE.Color("#c0703a") : n.kind === "leg" ? new THREE.Color("#2f6f8f") : col("--o"), roughness: 0.6, metalness: 0.05 });
      const m = new THREE.Mesh(geo, mat); m.position.copy(p); this.group.add(m);
      const div = document.createElement("div"); div.className = "lbl" + (isI ? " inst" : ""); div.textContent = isI ? instLabel : n.label;
      const o = new CSS2DObject(div); o.position.copy(p).add(new THREE.Vector3(0, isI ? 0.85 : 0.42, 0)); this.group.add(o);
    }
    for (const e of edges) {
      const a = pos.get(e.a)!, b = pos.get(e.b)!; const r = REL[e.rel] ?? REL.partners;
      const mid = a.clone().add(b).multiplyScalar(0.5).add(new THREE.Vector3(0, 0.35, 0));
      const curve = new THREE.QuadraticBezierCurve3(a, mid, b);
      const g = new THREE.BufferGeometry().setFromPoints(curve.getPoints(40));
      let line: THREE.Line;
      if (r.dash) { const mat = new THREE.LineDashedMaterial({ color: r.color, dashSize: 0.12, gapSize: 0.1 }); line = new THREE.Line(g, mat); line.computeLineDistances(); }
      else { const mat = new THREE.LineDashedMaterial({ color: r.color, dashSize: 0.35, gapSize: 0.06 }); line = new THREE.Line(g, mat); line.computeLineDistances(); if (!this.reduce) this.dashed.push(mat); }
      this.group.add(line);
      // arrow head at the target end
      const tip = curve.getPoint(0.88), dir = curve.getTangent(0.88);
      const cone = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.2, 10), new THREE.MeshBasicMaterial({ color: r.color }));
      cone.position.copy(tip); cone.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.normalize()); this.group.add(cone);
    }
  }
}
