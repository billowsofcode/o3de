/*
 * Copyright (c) Contributors to the Open 3D Engine Project.
 * For complete copyright and license terms please see the LICENSE at the root of this distribution.
 *
 * SPDX-License-Identifier: Apache-2.0 OR MIT
 *
 */

#pragma once

#include <AzCore/base.h>
#include <AzCore/Math/Aabb.h>
#include <AzCore/std/containers/array.h>
#include <AzCore/std/function/function_template.h>

#include <AzFramework/Terrain/TerrainDataRequestBus.h>

#include <TerrainRenderer/Aabb2i.h>
#include <TerrainRenderer/BindlessImageArrayHandler.h>
#include <TerrainRenderer/ClipmapBounds.h>
#include <TerrainRenderer/TerrainAreaMaterialRequestBus.h>
#include <TerrainRenderer/Vector2i.h>

#include <Atom/RPI.Public/Material/Material.h>
#include <Atom/RPI.Public/Image/AttachmentImage.h>
#include <Atom/RPI.Reflect/Image/Image.h>
#include <Atom/Feature/Utils/IndexedDataVector.h>
#include <Atom/Feature/Utils/SparseVector.h>
#include <Atom/Feature/Utils/GpuBufferHandler.h>

namespace Terrain
{
    class TerrainDetailMaterialManager
        : private AzFramework::Terrain::TerrainDataNotificationBus::Handler
        , private TerrainAreaMaterialNotificationBus::Handler
    {
    public:

        AZ_RTTI(TerrainDetailMaterialManager, "{3CBAF88F-E3B1-43B8-97A5-999133188BCC}");
        AZ_DISABLE_COPY_MOVE(TerrainDetailMaterialManager);

        TerrainDetailMaterialManager() = default;
        ~TerrainDetailMaterialManager() = default;
        
        void Initialize(
            const AZStd::shared_ptr<AZ::Render::BindlessImageArrayHandler>& bindlessImageHandler,
            AZ::Data::Instance<AZ::RPI::ShaderResourceGroup>& terrainSrg);
        bool IsInitialized() const;
        void Reset();
        bool UpdateSrgIndices(AZ::Data::Instance<AZ::RPI::ShaderResourceGroup>& srg);

        void Update(const AZ::Vector3& cameraPosition, AZ::Data::Instance<AZ::RPI::ShaderResourceGroup>& terrainSrg);

    private:
        
        using MaterialInstance = AZ::Data::Instance<AZ::RPI::Material>;
        static constexpr auto InvalidImageIndex = AZ::Render::BindlessImageArrayHandler::InvalidImageIndex;

        enum DetailTextureFlags : uint32_t
        {
            None                =  0b0000'0000'0000'0000'0000'0000'0000'0000,
            UseTextureBaseColor =  0b0000'0000'0000'0000'0000'0000'0000'0001,
            UseTextureNormal =     0b0000'0000'0000'0000'0000'0000'0000'0010,
            UseTextureMetallic =   0b0000'0000'0000'0000'0000'0000'0000'0100,
            UseTextureRoughness =  0b0000'0000'0000'0000'0000'0000'0000'1000,
            UseTextureOcclusion =  0b0000'0000'0000'0000'0000'0000'0001'0000,
            UseTextureHeight =     0b0000'0000'0000'0000'0000'0000'0010'0000,
            UseTextureSpecularF0 = 0b0000'0000'0000'0000'0000'0000'0100'0000,

            FlipNormalX =          0b0000'0000'0000'0001'0000'0000'0000'0000,
            FlipNormalY =          0b0000'0000'0000'0010'0000'0000'0000'0000,

            BlendModeMask =        0b0000'0000'0001'1100'0000'0000'0000'0000,
            BlendModeLerp =        0b0000'0000'0000'0100'0000'0000'0000'0000,
            BlendModeLinearLight = 0b0000'0000'0000'1000'0000'0000'0000'0000,
            BlendModeMultiply =    0b0000'0000'0000'1100'0000'0000'0000'0000,
            BlendModeOverlay =     0b0000'0000'0001'0000'0000'0000'0000'0000,
        };
        
        struct DetailMaterialShaderData
        {
            // Uv (data is 3x3, padding each row for explicit alignment)
            AZStd::array<float, 12> m_uvTransform
            {
                1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
            };

            float m_baseColorRed{ 1.0f };
            float m_baseColorGreen{ 1.0f };
            float m_baseColorBlue{ 1.0f };

            // Factor / Scale / Bias for input textures
            float m_baseColorFactor{ 1.0f };

            float m_normalFactor{ 1.0f };
            float m_metalFactor{ 0.0f };
            float m_roughnessScale{ 1.0f };
            float m_roughnessBias{ 0.0f };

            float m_specularF0Factor{ 0.5f };
            float m_occlusionFactor{ 1.0f };
            float m_heightFactor{ 1.0f };
            float m_heightOffset{ 0.0f };

            float m_heightBlendFactor{ 0.5f };

            // Flags
            DetailTextureFlags m_flags{ 0 };

            // Image indices
            uint16_t m_colorImageIndex{ InvalidImageIndex };
            uint16_t m_normalImageIndex{ InvalidImageIndex };
            uint16_t m_roughnessImageIndex{ InvalidImageIndex };
            uint16_t m_metalnessImageIndex{ InvalidImageIndex };

            uint16_t m_specularF0ImageIndex{ InvalidImageIndex };
            uint16_t m_occlusionImageIndex{ InvalidImageIndex };
            uint16_t m_heightImageIndex{ InvalidImageIndex };

            // 16 byte aligned
            uint16_t m_padding1{ 0 };
            uint32_t m_padding2{ 0 };
            uint32_t m_padding3{ 0 };
        };
        static_assert(sizeof(DetailMaterialShaderData) % 16 == 0, "DetailMaterialShaderData must be 16 byte aligned.");

        struct DetailMaterialData
        {
            AZ::Data::AssetId m_assetId;
            AZ::RPI::Material::ChangeId m_materialChangeId{AZ::RPI::Material::DEFAULT_CHANGE_ID};
            uint32_t m_refCount = 0;
            uint16_t m_detailMaterialBufferIndex{ 0xFFFF };

            AZ::Data::Instance<AZ::RPI::Image> m_colorImage;
            AZ::Data::Instance<AZ::RPI::Image> m_normalImage;
            AZ::Data::Instance<AZ::RPI::Image> m_roughnessImage;
            AZ::Data::Instance<AZ::RPI::Image> m_metalnessImage;
            AZ::Data::Instance<AZ::RPI::Image> m_specularF0Image;
            AZ::Data::Instance<AZ::RPI::Image> m_occlusionImage;
            AZ::Data::Instance<AZ::RPI::Image> m_heightImage;
        };

        struct DetailMaterialSurface
        {
            AZ::Crc32 m_surfaceTag;
            uint16_t m_detailMaterialId;
        };

        struct DetailMaterialListRegion
        {
            AZ::EntityId m_entityId;
            AZ::Aabb m_region{AZ::Aabb::CreateNull()};
            AZStd::vector<DetailMaterialSurface> m_materialsForSurfaces;
            uint16_t m_defaultDetailMaterialId{ 0xFFFF };

            bool HasMaterials()
            {
                return m_defaultDetailMaterialId != InvalidDetailMaterialId || !m_materialsForSurfaces.empty();
            }
        };
        
        using DetailMaterialContainer = AZ::Render::IndexedDataVector<DetailMaterialData>;
        static constexpr auto InvalidDetailMaterialId = DetailMaterialContainer::NoFreeSlot;
        
        // System-level parameters
        static constexpr int32_t DetailTextureSize{ 1024 };
        static constexpr int32_t DetailTextureSizeHalf{ DetailTextureSize / 2 };
        static constexpr float DetailTextureScale{ 0.5f };
        
        // AzFramework::Terrain::TerrainDataNotificationBus overrides...
        void OnTerrainDataChanged(const AZ::Aabb& dirtyRegion, TerrainDataChangedMask dataChangedMask) override;
        
        // TerrainAreaMaterialNotificationBus overrides...
        void OnTerrainDefaultSurfaceMaterialCreated(AZ::EntityId entityId, AZ::Data::Instance<AZ::RPI::Material> material) override;
        void OnTerrainDefaultSurfaceMaterialDestroyed(AZ::EntityId entityId) override;
        void OnTerrainDefaultSurfaceMaterialChanged(AZ::EntityId entityId, AZ::Data::Instance<AZ::RPI::Material> newMaterial) override;
        void OnTerrainSurfaceMaterialMappingCreated(AZ::EntityId entityId, SurfaceData::SurfaceTag surfaceTag, MaterialInstance material) override;
        void OnTerrainSurfaceMaterialMappingDestroyed(AZ::EntityId entityId, SurfaceData::SurfaceTag surfaceTag) override;
        void OnTerrainSurfaceMaterialMappingMaterialChanged(AZ::EntityId entityId, SurfaceData::SurfaceTag surfaceTag, MaterialInstance material) override;
        void OnTerrainSurfaceMaterialMappingTagChanged(
            AZ::EntityId entityId, SurfaceData::SurfaceTag oldSurfaceTag, SurfaceData::SurfaceTag newSurfaceTag) override;
        void OnTerrainSurfaceMaterialMappingRegionCreated(AZ::EntityId entityId, const AZ::Aabb& region) override;
        void OnTerrainSurfaceMaterialMappingRegionDestroyed(AZ::EntityId entityId, const AZ::Aabb& oldRegion) override;
        void OnTerrainSurfaceMaterialMappingRegionChanged(AZ::EntityId entityId, const AZ::Aabb& oldRegion, const AZ::Aabb& newRegion) override;

        //! Removes all images from all detail materials from the bindless image array
        void RemoveAllImages();

        //! Creates or updates an existing detail material with settings from a material instance
        uint16_t CreateOrUpdateDetailMaterial(MaterialInstance material);

        //! Decrements the ref count on a detail material and removes it if it reaches 0
        void CheckDetailMaterialForDeletion(uint16_t detailMaterialId);

        //! Updates a specific detail material with settings from a material instance
        void UpdateDetailMaterialData(uint16_t detailMaterialIndex, MaterialInstance material);

        //! Checks to see if the detail material id texture needs to update based on the camera position. Any
        //! required updates are then executed.
        void CheckUpdateDetailTexture(const AZ::Vector3& cameraPosition);

        //! Updates the detail texture in a given area
        void UpdateDetailTexture(const AZ::Aabb& worldUpdateAabb, const Aabb2i& textureUpdateAabb);

        //! Finds the detail material Id for a region and surface type
        uint16_t GetDetailMaterialForSurfaceType(const DetailMaterialListRegion& materialRegion, AZ::Crc32 surfaceType) const;

        //! Finds a region for a position. Returns nullptr if none found.
        const DetailMaterialListRegion* FindRegionForPosition(const AZ::Vector2& position) const;
    
        //! Initializes shader data for the default passthrough material which is used when no other detail material is found.
        void InitializePassthroughDetailMaterial();

        using DefaultMaterialSurfaceCallback = AZStd::function<void(DetailMaterialSurface&)>;
        bool ForSurfaceTag(DetailMaterialListRegion& materialRegion,
            SurfaceData::SurfaceTag surfaceTag, DefaultMaterialSurfaceCallback callback);
        DetailMaterialListRegion* FindByEntityId(AZ::EntityId entityId, AZ::Render::IndexedDataVector<DetailMaterialListRegion>& container);
        DetailMaterialListRegion& FindOrCreateByEntityId(AZ::EntityId entityId, AZ::Render::IndexedDataVector<DetailMaterialListRegion>& container);
        void RemoveByEntityId(AZ::EntityId entityId, AZ::Render::IndexedDataVector<DetailMaterialListRegion>& container);

        AZStd::shared_ptr<AZ::Render::BindlessImageArrayHandler> m_bindlessImageHandler;
        
        AZ::Data::Instance<AZ::RPI::AttachmentImage> m_detailTextureImage;

        DetailMaterialContainer m_detailMaterials;
        AZ::Render::IndexedDataVector<DetailMaterialListRegion> m_detailMaterialRegions;
        AZ::Render::SparseVector<DetailMaterialShaderData> m_detailMaterialShaderData;
        AZ::Render::GpuBufferHandler m_detailMaterialDataBuffer;
        uint8_t m_passthroughMaterialId = 0;

        AZ::Aabb m_dirtyDetailRegion{ AZ::Aabb::CreateNull() };
        ClipmapBounds m_detailMaterialIdBounds;

        AZ::RHI::ShaderInputImageIndex m_detailMaterialIdPropertyIndex;
        AZ::RHI::ShaderInputBufferIndex m_detailMaterialDataIndex;
        AZ::RHI::ShaderInputConstantIndex m_detailScalePropertyIndex;

        bool m_isInitialized{ false };
        bool m_detailMaterialBufferNeedsUpdate{ false };
        bool m_detailImageNeedsUpdate{ false };
        
    };
}
