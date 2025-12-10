<template>
  <div class="app-shell">
    <Toast position="top-right" />
    <header class="hero">
      <div class="hero-logo-shell">
        <img :src="JRAutomationLogo" alt="JRAutomation logo" class="hero-logo" />
      </div>
      <div class="hero-copy">
        <h1 class="section-title">Laboratory Knowledge Console</h1>
        <p class="subtle">Upload lab documents, process them, and ask precise questions with traceable sources.</p>
      </div>
    </header>

    <div class="grid">
      <div class="column">
        <Card class="card upload" >
          <template #title>
            <div class="card-head">
              <Tag value="Max 10 files · 10MB each" severity="info" />
            </div>
          </template>
          <template #content>
            
          <FileUpload
            ref="fileUploader"
            name="files"
            :customUpload="true"
            @uploader="onUploadFiles"
            :multiple="true"
            accept=".pdf,.md,.markdown,.txt,.docx"
            :maxFileSize="10485760"
          >
              <template #empty>
                <div class="drop-hint">
                  <i class="pi pi-cloud-upload" style="font-size: 2rem"></i>
                  <div>Drag and drop files here to upload</div>
                  <div class="subtle mb-3">Accepted: PDF, Markdown, DOCX, TXT.</div>
                </div>
              </template>
            <template #upload-status>
              <div class="upload-status" v-if="uploadProgressLabel">
                <i :class="{
                  'pi pi-check-circle icon-success': uploadProgress === 100,
                  'pi pi-info-circle icon-warn': uploadProgress > 0 && uploadProgress < 100,
                  'pi pi-cloud-upload icon-muted': uploadProgress === 0
                }"></i>
                <span>{{ uploadProgressLabel }}</span>
              </div>
            </template> 
          </FileUpload>
          <Divider />
          <div class="p-grid p-nogutter p-align-center gap-2">
            <div class="actions-row">
              <Button
                label="Process"
                icon="pi pi-cog"
                class="p-button-raised ml-3"
                :loading="processing"
                :disabled="!canProcess"
                @click="onProcess"
              />
              <Button
                label="Reset"
                icon="pi pi-refresh"
                class="mr-3 small"
                :loading="resetting"
                :disabled="!canReset"
                @click="onReset"
              />
            </div>
          </div>
            <div class="mt-3" v-if="processing || progressValue > 0">
              <div class="progress-shell">
                <ProgressBar :value="progressValue" :showValue="false" />
              </div>
              <div class="subtle mt-1">{{ progressLabel }}</div>
            </div>
            <div class="uploaded" v-if="uploadedFiles.length">
              <div class="uploaded-head">
                <span>Uploaded</span>
                <Tag :value="uploadedFiles.length" severity="info" />
              </div>
              <ul class="uploaded-list">
                <li v-for="file in uploadedFiles" :key="file">
                  <i class="pi pi-upload"></i>
                  <span>{{ file }}</span>
                </li>
              </ul>
            </div>
            <div class="processed" v-if="processedFiles.length">
              <div class="processed-head">
                <span>Processed files</span>
                <Tag :value="processedFiles.length" severity="success" />
              </div>
              <ul class="processed-list">
                <li v-for="file in processedFiles" :key="file">
                  <i class="pi pi-check-circle"></i>
                  <span>{{ file }}</span>
                </li>
              </ul>
            </div>
          </template>
        </Card>
 
   

        <Card class="card info">
          <template #title>
            <div class="card-head">
              <span>Session Test Limits</span>
              <Tag value="Safety" severity="success" />
            </div>
          </template>
          <template #subtitle>
            <div class="subtle">For demonstration purposes only.</div>
          </template>
          <template #content>
            <ul class="limits">
              <li>Up to 10 files.</li>
              <li>Max 10MB per file.</li>
              <li>Sources are shown with filename and page.</li>
              <li>Docs live in memory only for this proof of concept.</li>
            </ul>
          </template>
  
        </Card>
      </div>

      <div class="column chat">
        <Card class="card">
          <template #title>
            <div class="card-head">
              <span>Lab Chat</span>
              <Tag :value="chunksTag" severity="info" />
            </div>
          </template>
          <template #content>
            <div class="chat-window glass">
              <ScrollPanel style="width: 100%; height: 420px">
                <div v-if="!chatLog.length" class="placeholder subtle">
                  Ask about procedures, safety steps, or robot behaviors once documents are processed.
                </div>
                <div v-for="(entry, index) in chatLog" :key="index" :class="['bubble', entry.role]">
                  <div class="bubble-head">
                    <span>{{ entry.role === 'user' ? 'You' : 'Lab Assistant' }}</span>
                    <span class="timestamp">{{ entry.time }}</span>
                  </div>
                  <div class="bubble-text">{{ entry.text }}</div>
                </div>
              </ScrollPanel>
            </div>
            <div class="question-box">
              <label>Question</label>
              <Textarea
                v-model="question"
                autoResize
                rows="3"
                placeholder="How do we calibrate the robot arm?"

              />
              <div class="actions">
                <Button
                  label="Send"
                  icon="pi pi-send"
                  :loading="asking"
                  :disabled="!canAsk"
                  @click="askQuestion"
                />
              </div>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </div>
  <footer class="page-footer">
    <div class="footer-content">
      <div class="footer-meta">
        <span>© 2025. Product rights reserved for JRAutomation.</span>
        <span>Built with third-party licenses apply per their terms.</span>
      </div>
       <div class="footer-logos">
        <img :src="companyForBusiness" alt="N6 logo" class="footer-logo" />
        <span class="footer-note">Designed for N6</span>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed, ref } from "vue";
import { useToast } from "primevue/usetoast";
import { format } from "date-fns";
import { processDocuments, queryRag, resetDocuments, uploadDocuments } from "./services/api";
import companyForBusiness from "./assets/n6Logo.png";
import JRAutomationLogo from "./assets/JRautomationLogo.png";

const toast = useToast();
const uploadStatus = ref(null);
const processing = ref(false);
const progressValue = ref(0);
const uploadProgress = ref(0);
const uploading = ref(false);
const chunksCount = ref(0);
const resetting = ref(false);
const question = ref("");
const asking = ref(false);
const chatLog = ref([]);
const processedFiles = ref([]);
const fileUploader = ref(null);
const uploadedFiles = computed(() => uploadStatus.value?.uploaded || []);

const filesCount = computed(
  () => uploadStatus.value?.total_files || uploadedFiles.value.length || 0
);
const canAsk = computed(() =>  chunksCount.value > 0 && question.value.trim().length > 2 && !asking.value);
const canProcess = computed(() => filesCount.value > 0 && !processing.value && !uploading.value);
const canReset = computed(
  () =>
    (filesCount.value > 0 || processedFiles.value.length > 0 || chunksCount.value > 0) &&
    !processing.value &&
    !uploading.value &&
    !resetting.value
);
const progressLabel = computed(() => {
  if (processing.value) return "Processing documents";
  if (progressValue.value === 100) return "Ready";
  if (progressValue.value > 0) return "Finalizing";
  return "";
});

const chunksTag = computed(() => `${chunksCount.value} chunks ready`);
const uploadProgressLabel = computed(() =>
  uploading.value ? `Uploading... ${uploadProgress.value}%` : uploadProgress.value === 100 ? "Uploaded" : ""
);


const timestamp = () => format(new Date(), "HH:mm:ss");


const errorDetail = (error) => error?.response?.data?.detail || "Unexpected error";

const onUploadFiles = async (event) => {
  const files = event?.files || [];
  if (!files.length) {
    toast.add({ severity: "info", summary: "No files", detail: "Select at least one file", life: 2500 });
    return;
  }
  const processedSet = new Set(processedFiles.value);
  const filteredFiles = files.filter((file) => !processedSet.has(file.name));
  if (filteredFiles.length !== files.length) {
    toast.add({
      severity: "warn",
      summary: "Duplicate",
      detail: "Some files were already processed and were skipped",
      life: 3000,
    });
  }
  if (!filteredFiles.length) {
    toast.add({ severity: "info", summary: "No new files", detail: "All selected files were already processed", life: 3000 });
    return;
  }
  try {
    uploadProgress.value = 0;
    uploading.value = true;
    const data = await uploadDocuments(filteredFiles, (progressEvent) => {
      if (!progressEvent.total) return;
      uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
    });
    uploadStatus.value = data;
    chunksCount.value = 0;
    toast.add({ severity: "success", summary: "Uploaded", detail: `Accepted ${data.uploaded.length} file(s)`, life: 3000 });
    if (event?.options?.clear) {
      event.options.clear();
    } else if (fileUploader.value?.clear) {
      fileUploader.value.clear();
    }
  } catch (error) {
    const detail = errorDetail(error);
    toast.add({ severity: "error", summary: "Upload", detail, life: 4000 });
  } finally {
    uploading.value = false;
    uploadProgress.value = 0;}
};

const simulateProgress = async () => {
  progressValue.value = 15;
  await new Promise((resolve) => setTimeout(resolve, 300));
  progressValue.value = 45;
  await new Promise((resolve) => setTimeout(resolve, 300));
  progressValue.value = 70;
};

const onProcess = async () => {
  processing.value = true;
  try {
    await simulateProgress();
    const data = await processDocuments();
    progressValue.value = 100;
    chunksCount.value = data.chunks;
    const newlyProcessed = uploadStatus.value?.uploaded || [];
    processedFiles.value = Array.from(new Set([...processedFiles.value, ...newlyProcessed]));
    uploadStatus.value = null;
    toast.add({ severity: "success", summary: "Processed", detail: `${data.chunks} chunks ready`, life: 3000 });
  } catch (error) {
    const detail = errorDetail(error);
    toast.add({ severity: "error", summary: "Process", detail, life: 4000 });
  } finally {
    processing.value = false;
    setTimeout(() => (progressValue.value = 0), 800);
  }
};

const onReset = async () => {
  if (!canReset.value) return;
  resetting.value = true;
  try {
    const data = await resetDocuments();
    uploadStatus.value = null;
    chunksCount.value = 0;
    progressValue.value = 0;
    uploadProgress.value = 0;
    processedFiles.value = [];
    chatLog.value = [];
    question.value = "";
    if (fileUploader.value?.clear) {
      fileUploader.value.clear();
    }
    toast.add({ severity: "success", summary: "Reset", detail: `${data.files_cleared} file(s) cleared`, life: 3000 });
  } catch (error) {
    const detail = errorDetail(error);
    toast.add({ severity: "error", summary: "Reset", detail, life: 4000 });
  } finally {
    resetting.value = false;
  }
};

const askQuestion = async () => {
  if (!canAsk.value) return;
  const q = question.value.trim();
  question.value = "";
  chatLog.value.push({ role: "user", text: q, time: timestamp() });
  asking.value = true;
  try {
    const data = await queryRag(q);
    chatLog.value.push({ role: "assistant", text: data.answer, time: timestamp(), sources: data.chunks });
  } catch (error) {
    const detail = errorDetail(error);
    toast.add({ severity: "error", summary: "Chat", detail, life: 4000 });
  } finally {
    asking.value = false;
  }
};
</script>

<style scoped>
.app-shell {
  padding: 1.5rem;
  max-width: 1500px;
  margin: 0 auto;
  padding-bottom: 8rem;
}

.hero {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: 2rem;
}

.hero-copy {
  flex: 1;
}

.hero-logo-shell {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 200px;
}

.hero-logo {
  height: 160px;
  width: auto;
  max-width: 360px;
  object-fit: contain;
  filter: drop-shadow(0 4px 4px rgba(0, 0, 0, 0.12));
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 1.25rem;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card {
  border-radius: 16px;
  overflow: hidden;
}

.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.01em;
}

.subtle{
  margin-bottom: 2px;
}

.upload .p-fileupload {
  width: 100%;
  height:50%;
}

.drop-hint {
  text-align: center;
  padding: 1.25rem;
  color: var(--muted);
}

.upload-status {
  margin-top: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.limits {
  padding-left: 1.1rem;
  color: var(--muted);
  line-height: 1.7;
}

.chat .card {
  min-height: 720px;
}

.chat-window {
  border-radius: 14px;
  border: 1px solid var(--border);
  padding: 0.75rem;
  margin-bottom: 1rem;
}

.placeholder {
  padding: 1rem;
}

.bubble {
  padding: 0.9rem;
  margin-bottom: 0.9rem;
  border-radius: 12px;
  border: 1px solid var(--border);
}

.bubble.user {
  background: rgba(15, 118, 110, 0.08);
  border-color: rgba(15, 118, 110, 0.25);
}

.bubble.assistant {
  background: #f1f5f9;
}

.bubble-head {
  display: flex;
  justify-content: space-between;
  color: #475569;
  font-weight: 600;
  margin-bottom: 0.45rem;
}

.bubble-text {
  margin: 0;
  color: #0f172a;
  line-height: 1.5;
  white-space: pre-wrap;
}

.question-box {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.actions {
  display: flex;
  justify-content: flex-end;
}

.actions-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  justify-content: space-between;
}

.processed {
  margin-top: 1rem;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 0.75rem;
}

.uploaded {
  margin-top: 1rem;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 0.75rem;
}

.uploaded-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.uploaded-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.35rem;
}

.uploaded-list li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #0f172a;
}

.uploaded-list i {
  color: #0ea5e9;
}

.processed-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.processed-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 0.35rem;
}

.processed-list li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #0f172a;
}

.processed-list i {
  color: #22c55e;
}

.timestamp {
  color: #94a3b8;
  font-size: 0.85rem;
}

.icon-success {
  color: #34d399;
  margin-right: 0.35rem;
}

.icon-warn {
  color: #fbbf24;
  margin-right: 0.35rem;
}

.icon-muted {
  color: var(--muted);
  margin-right: 0.35rem;
}

@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
    align-items: flex-start;
  }
  .chat .card {
    min-height: auto;
  }
  .hero-logo-shell {
    align-self: flex-start;
    min-width: auto;
    margin-top: 0.5rem;
  }
  .hero-logo {
    height: 120px;
    max-width: 280px;
  }
}

.page-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(90deg, rgba(15, 118, 110, 0.08), rgba(14, 116, 144, 0.08));
  border-top: 1px solid var(--border);
  backdrop-filter: blur(8px);
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0.9rem 1.5rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 0.75rem;
  align-items: center;
}

.footer-logos {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.footer-logo {
  height: 36px;
  width: auto;
  display: block;
}

.footer-note {
  color: #0f172a;
  font-weight: 600;
  letter-spacing: 0.01em;
}

.footer-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--muted);
  font-size: 0.95rem;
}

@media (max-width: 640px) {
  .footer-content {
    flex-direction: column;
    align-items: flex-start;
  }
  .footer-meta {
    flex-wrap: wrap;
    gap: 0.35rem;
  }
}
</style>
